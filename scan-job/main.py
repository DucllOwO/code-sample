import argparse
import asyncio
from time import sleep
from src.configs import settings
from src.services.web3_service import Web3Service
from src.configs import postgres_database
from src.services.scan_configuration_service import ScanConfigurationService
from src.constant import EventNameEnum
from src.services.donor_service import DonorService
from src.services.analytic_service import AnalyticService
from src.services.withdraw_service import WithdrawService
import binascii
from sqlalchemy.orm import Session
from src.services.transaction_tracking_service import TransactionTrackingService
import logging


class Scanner:
    def __init__(self, chain_id: int, event_name: EventNameEnum):
        self.config = ScanConfigurationService.get_scan_configuration(
            chain_id, event_name, postgres_database.dynamic_session())
        self.event_name = event_name
        self.chain_id = chain_id
        self.current_block_number = int(
            self.config.get("scanned_block_number"))
        self.web3_service = Web3Service(self.config.get("rpc_provider"))
        self.contract = self.web3_service.get_contract(
            contract_address=self.config.get("contract_address"), abi=[self.config.get("abi")])

    def get_to_block(self, current_block_number):
        latest_block_number = self.web3_service.web3.eth.block_number

        if current_block_number + settings.BLOCKS_PER_TIME < latest_block_number:
            return int(current_block_number + settings.BLOCKS_PER_TIME)
        return int(latest_block_number)

    def get_setup_each_scan(self, chain_id: int, event_name: str):
        self.config = ScanConfigurationService.get_scan_configuration(
            chain_id, event_name, postgres_database.dynamic_session())
        self.current_block_number = int(
            self.config.get("scanned_block_number"))
        self.contract = self.web3_service.get_contract(
            contract_address=self.config.get("contract_address"), abi=[self.config.get("abi")])
        self.web3_service = Web3Service(self.config.get("rpc_provider"))

    async def scan_transaction(self):
        session = postgres_database.dynamic_session()
        while True:
            self.get_setup_each_scan(self.chain_id, self.event_name)

            to_block_number = self.get_to_block(self.current_block_number)
            logging.info("scan from block to block: {0} {1}".format(
                self.current_block_number, to_block_number))
            if self.current_block_number <= to_block_number:

                with session.begin():
                    event_data = self.web3_service.parse_event_data(
                        self.contract, to_block_number, self.current_block_number, self.event_name)

                    if event_data is not None:
                        for event in event_data:
                            tx_hash = event.get("transactionHash").hex()
                            if TransactionTrackingService.is_tx_hash_exist(tx_hash, session) is True:
                                logging.info(
                                    f"Transaction {tx_hash} was scanned. Skip to next transaction")
                                continue

                            self.handle_process_event_data(event, session)
                            TransactionTrackingService.record_scanned_transaction(
                                tx_hash, session)
                            session.flush()

                    self.current_block_number = to_block_number

                    ScanConfigurationService.update_scanned_block_number(
                        self.chain_id, self.event_name, to_block_number, session)

            # sleep for a while before next block
            sleep(settings.BLOCK_SLEEP_TIME)

    def handle_process_event_data(self, event_data: dict, session: Session):
        match self.event_name:
            case EventNameEnum.buy_token.value:
                args = event_data.get("args")
                contract_mapping_id = '0x' + \
                    binascii.hexlify(args.get("proID")).decode('utf-8')
                DonorService.handle_insert_donor(
                    self.chain_id,
                    event_data.get("transactionHash").hex(),
                    {
                        "round": args.get("round"),
                        "amount_token": args.get("amountToken"),
                        "amount_native": args.get("price"),
                        "contract_mapping_id": contract_mapping_id,
                        "address": args.get("from")
                    },
                    session)
                AnalyticService.update_analytic_of_project_base_on_chain(
                    contract_mapping_id, self.chain_id, args.get("price"), args.get("amountToken"), args.get("round"), session)
                logging.info("Process buy token success")
            case EventNameEnum.investor.value:
                args = event_data.get("args")
                contract_mapping_id = '0x' + \
                    binascii.hexlify(args.get("proID")).decode('utf-8')
                DonorService.handle_insert_donor(
                    self.chain_id,
                    event_data.get("transactionHash").hex(),
                    {
                        "round": args.get("round"),
                        "amount_token": args.get("ticket"),
                        "amount_native": args.get("amount"),
                        "contract_mapping_id": contract_mapping_id,
                        "address": args.get("from")
                    },
                    session)
                AnalyticService.update_analytic_of_project_base_on_chain(
                    contract_mapping_id, self.chain_id, args.get("amount"), args.get("ticket"), args.get("round"), session)
                logging.info("Process event investor success")
            case EventNameEnum.withdraw.value:
                args = event_data.get("args")
                logging.info(args)
                contract_mapping_id = '0x' + \
                    binascii.hexlify(args.get("proID")).decode('utf-8')
                WithdrawService.handle_insert_withdraw(
                    self.chain_id,
                    event_data.get("transactionHash").hex(),
                    {
                        "round": args.get("round"),
                        "amount_token": args.get("ticket"),
                        "amount_native": args.get("amount"),
                        "contract_mapping_id": contract_mapping_id,
                        "address": args.get("from")
                    },
                    session)
                AnalyticService.handle_withdraw_donate(
                    contract_mapping_id, self.chain_id, args.get("amount"), args.get("ticket"), args.get("round"), session)
                logging.info("Process event withdraw success")


if __name__ == "__main__":
    # This sets the root logger to write to stdout (your console).
    # Your script/app needs to call this somewhere at least once.
    logging.basicConfig()

    # By default the root logger is set to WARNING and all loggers you define
    # inherit that value. Here we set the root logger to NOTSET. This logging
    # level is automatically inherited by all existing and new sub-loggers
    # that do not set a less verbose level.
    logging.root.setLevel(logging.DEBUG)

    # The following line sets the root logger level as well.
    # It's equivalent to both previous statements combined:
    # logging.basicConfig(level=logging.NOTSET)
    logging.basicConfig(
        level=logging.NOTSET,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logging.info("Starting...")
    asyncio.run(postgres_database.on_start())

    # get param from command line
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-e",
        "--event",
        type=str,
        help="Name of event (BuyToken, RegisterEvent, Withdraw, Investor)",
    )
    parser.add_argument(
        "-c",
        "--chain",
        type=int,
        help="Chain id (Binance(97), Fantom(4002))",
    )
    args = parser.parse_args()

    # scan data
    scanner = Scanner(args.chain, args.event)

    asyncio.run(scanner.scan_transaction())
