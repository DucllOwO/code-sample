from src.models import postgres_model
from sqlalchemy.orm import Session
from src.util import convert_record_to_dict


class ScanConfigurationService:
    @classmethod
    def get_scan_configuration(self, chain_id: int, event_name: str, db: Session):
        config = db.query(postgres_model.ScanConfiguration).filter(
            postgres_model.ScanConfiguration.chain_id == chain_id, postgres_model.ScanConfiguration.event == event_name).first()

        if config is None:
            raise Exception(
                f"Configuration for event {event_name} and chain {chain_id} not found")

        return config.__dict__

    @classmethod
    def update_scanned_block_number(self, chain_id: int, event_name: str, new_block_number: int, db: Session):
        config = db.query(postgres_model.ScanConfiguration).filter(
            postgres_model.ScanConfiguration.chain_id == chain_id, postgres_model.ScanConfiguration.event == event_name).first()

        config.scanned_block_number = new_block_number
