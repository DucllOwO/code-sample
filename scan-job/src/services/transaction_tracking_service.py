

from sqlalchemy.orm import Session
from src.models.postgres_model import TransactionTracking


class TransactionTrackingService:
    @classmethod
    def record_scanned_transaction(self, tx_hash: str, db: Session):
        return db.add(TransactionTracking(tx_hash=tx_hash))

    @classmethod
    def is_tx_hash_exist(self, tx_hash: str, db: Session):
        return db.query(TransactionTracking).filter(TransactionTracking.tx_hash == tx_hash).first() is not None
