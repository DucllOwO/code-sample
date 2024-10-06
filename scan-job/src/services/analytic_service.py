from src.models.postgres_model import Analytic
from sqlalchemy.orm import Session
from src.constant import AnalyticChainFieldMapping
import logging


class AnalyticService:
    @classmethod
    def create_analytic(self, contract_mapping_id: str, round: str, db: Session):
        analytic = Analytic(
            contract_mapping_id=contract_mapping_id, round=round)
        db.add(analytic)
        return analytic

    @classmethod
    def update_analytic_of_project_base_on_chain(self, contract_mapping_id: str, chain_id: str, amount_native: int, amount_token: int, round: str, db: Session):
        analytic = db.query(Analytic).filter(
            Analytic.contract_mapping_id == contract_mapping_id, Analytic.round == round).first()

        if analytic is None:
            analytic = self.create_analytic(contract_mapping_id, round, db)
            db.flush()
            logging.info(
                f"Create new analytic for contract_mapping_id {contract_mapping_id}")

         # Using getattr and setattr for dynamic attribute access
        chain_field = AnalyticChainFieldMapping[str(chain_id)]
        current_native_amount = getattr(analytic, chain_field, 0)
        setattr(analytic, chain_field, int(
            current_native_amount) + int(amount_native))

        # Update total amount sold unit
        current_total_amount_sold_unit = getattr(
            analytic, 'total_amount_sold_unit', 0)
        setattr(analytic, 'total_amount_sold_unit',
                int(current_total_amount_sold_unit) + int(amount_token))

    @classmethod
    def handle_withdraw_donate(self, contract_mapping_id: str, chain_id: str, amount_native: int, amount_token: int, round: str, db: Session):
        analytic = db.query(Analytic).filter(
            Analytic.contract_mapping_id == contract_mapping_id, Analytic.round == round).first()

        chain_field = AnalyticChainFieldMapping[str(chain_id)]

        current_native_amount = getattr(analytic, chain_field, 0)
        setattr(analytic, chain_field, int(
            current_native_amount) - int(amount_native))

        # Update total amount sold unit
        current_total_amount_sold_unit = getattr(
            analytic, 'total_amount_sold_unit', 0)
        setattr(analytic, 'total_amount_sold_unit',
                int(current_total_amount_sold_unit) - int(amount_token))
