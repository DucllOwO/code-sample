from sqlalchemy.orm import Session
from src.models import postgres_model
import logging


class DonorService:
    @classmethod
    def get_donor_by_tx_hash(self, tx_hash: str, db: Session) -> postgres_model.Donor:
        return db.query(postgres_model.Donor).filter(postgres_model.Donor.tx_hash == tx_hash).first()

    @classmethod
    def insert_donor(self, data: dict, db: Session):
        donor = postgres_model.Donor(**data)
        db.add(donor)

    @classmethod
    def handle_insert_donor(self, chain_id: int, tx_hash: str, data: dict, db: Session):
        donor = self.get_donor_by_tx_hash(tx_hash, db)

        if donor is not None:
            logging.info(f"Warning: tx_hash {tx_hash} is already exist")
            # raise Exception(f"Donate transaction is already existed")
            return

        self.insert_donor(
            {**data, "chain_id": chain_id, "tx_hash": tx_hash}, db)
