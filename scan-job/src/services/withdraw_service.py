from sqlalchemy.orm import Session
from src.models import postgres_model
import logging


class WithdrawService:
  @classmethod
  def get_withdraw_by_tx_hash(self, tx_hash: str, db: Session) -> postgres_model.Withdraw:
      return db.query(postgres_model.Withdraw).filter(postgres_model.Withdraw.tx_hash == tx_hash).first()

  @classmethod
  def insert_withdraw(self, data: dict, db: Session):
      withdraw = postgres_model.Withdraw(**data)
      db.add(withdraw)

  @classmethod
  def handle_insert_withdraw(self, chain_id: int, tx_hash: str, data: dict, db: Session):
      withdraw = self.get_withdraw_by_tx_hash(tx_hash, db)

      if withdraw is not None:
          logging.info(f"Warning: tx_hash {tx_hash} is already exist")
          # raise Exception(f"Donate transaction is already existed")
          return

      self.insert_withdraw(
          {**data, "chain_id": chain_id, "tx_hash": tx_hash}, db)
