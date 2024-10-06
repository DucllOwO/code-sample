from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Column,
    Float,
    Integer,
    ForeignKey,
    func,
    String,
    ARRAY,
    text,
    TIMESTAMP,
    DECIMAL,
    Text,
    Enum,
    JSON,
    INTEGER,
    Identity,
    Boolean
)
from src.configs.postgres_database import Base
from typing import List
from src.constant import EventNameEnum, RoundEnum


class Project(Base):
    __tablename__ = "project"

    id = Column(UUID(as_uuid=True), primary_key=True,
                server_default=text("gen_random_uuid()"))
    whitepage_id = Column(UUID(as_uuid=True), ForeignKey('whitepage.id'))
    contract_mapping_id = Column(String)
    origin_chain_id = Column(String)
    name = Column(String)
    description = Column(String)
    token_address = Column(String)
    owner = Column(String)
    logo = Column(String)
    banner = Column(String)
    email = Column(String)
    fee = Column(Float, default=0.05)
    currency = Column(String)
    eligibility = Column(String)
    symbol = Column(String)
    demo = Column(String)
    thumbnail = Column(String)
    register_status = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
    deleted_at = Column(TIMESTAMP(timezone=True))


class Presale(Base):
    __tablename__ = "presale"

    id = Column(UUID(as_uuid=True), primary_key=True,
                server_default=text("gen_random_uuid()"))
    eligibility = Column(String)
    chain_ids = Column(ARRAY(String))
    tx_hash = Column(String)
    progress = Column(String, default='0%')
    start_time = Column(TIMESTAMP(timezone=True))
    end_time = Column(TIMESTAMP(timezone=True))
    softcap = Column(String)
    hardcap = Column(String)
    token_presale = Column(String)
    total_supply = Column(String)
    price = Column(DECIMAL)
    token_per_ticket = Column(String)
    per_ticket_value_usd = Column(DECIMAL)
    max_contribution_per_user = Column(Integer)
    project_id = Column(UUID, ForeignKey("project.id"))
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
    deleted_at = Column(TIMESTAMP(timezone=True))


class PublicSale(Base):
    __tablename__ = "public_sale"

    id = Column(UUID(as_uuid=True), primary_key=True,
                server_default=text("gen_random_uuid()"))
    eligibility = Column(String)
    min_buy_per_transaction = Column(Float)
    max_buy_per_user = Column(Float)
    project_id = Column(UUID, ForeignKey("project.id"))
    chain_ids = Column(ARRAY(Text))
    tx_hash = Column(String)
    progress = Column(String, default='0%')
    start_time = Column(TIMESTAMP(timezone=True))
    end_time = Column(TIMESTAMP(timezone=True))
    sell_amount = Column(String)
    sell_rate_per_usd = Column(DECIMAL)
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
    deleted_at = Column(TIMESTAMP(timezone=True))


class ScanConfiguration(Base):
    __tablename__ = "scan_configuration"

    id = Column(UUID(as_uuid=True), primary_key=True,
                server_default=text("gen_random_uuid()"))

    chain_id = Column(Integer)
    event = Column(String, Enum(EventNameEnum))
    contract_address = Column(String)
    rpc_provider = Column(String)
    abi = Column(JSON)
    scanned_block_number = Column(INTEGER, default='0')
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())


class Analytic(Base):
    __tablename__ = "analytic"

    id = Column(UUID(as_uuid=True), primary_key=True,
                server_default=text("gen_random_uuid()"))
    round = Column(Enum(RoundEnum))
    total_amount_sold_unit = Column(String, nullable=False, default='0')
    contract_mapping_id = Column(String, nullable=False)
    ethereum = Column(String, nullable=False, default='0')
    binance = Column(String, nullable=False, default='0')
    fantom = Column(String, nullable=False, default='0')
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
    deleted_at = Column(TIMESTAMP(timezone=True))


class Donor(Base):
    __tablename__ = "donor"

    id = Column(UUID(as_uuid=True), primary_key=True,
                server_default=text("gen_random_uuid()"))
    tx_hash = Column(String)
    chain_id = Column(String)
    round = Column(Enum(RoundEnum))
    amount_token = Column(String)
    amount_native = Column(String)
    address = Column(String)
    contract_mapping_id = Column(String)
    is_claimed = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
    deleted_at = Column(TIMESTAMP(timezone=True))


class Withdraw(Base):
    __tablename__ = "withdraw"

    id = Column(UUID(as_uuid=True), primary_key=True,
                server_default=text("gen_random_uuid()"))
    tx_hash = Column(String)
    chain_id = Column(String)
    round = Column(Enum(RoundEnum))
    amount_token = Column(String)
    amount_native = Column(String)
    address = Column(String)
    contract_mapping_id = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
    deleted_at = Column(TIMESTAMP(timezone=True))


class TransactionTracking(Base):
    __tablename__ = "transaction_tracking"

    id = Column("id", Integer, Identity(),
                primary_key=True, autoincrement=True)
    tx_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
