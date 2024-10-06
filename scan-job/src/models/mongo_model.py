from beanie import Document, Link
from typing import Optional
from pydantic import BaseModel, ConfigDict


class RoundAnalytics(Document):
    round: str
    ethereum: float = 0
    binance: float = 0
    fantom: float = 0
    total: float = 0
    ticket: int = 0
    pro_id: str = ""

    class Settings:
        name = "round_analytics"


class Analytics(Document):
    round_analytics: Link[RoundAnalytics]
    total: float = 0
    total_ticket: int = 0
    pro_id: str = ""

    class Settings:
        name = "analytics"


class Transaction(Document):
    tx_hash: str
    event: str

    class Settings:
        name = "transactions"


class BlockTracking(Document):
    chain_id: int
    event: str
    from_block: int

    class Settings:
        name = "block_tracking"


class Contract(Document):
    chain_id: int
    event: str
    contract: str

    class Settings:
        name = "contract"
