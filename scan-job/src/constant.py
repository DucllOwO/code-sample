from enum import Enum


class ChainNameEnum(Enum):
    binance: str = "binance"
    fantom: str = "fantom"


AnalyticChainFieldMapping = {
    "97": "binance",
    "4002": "fantom",
    "11155111": 'ethereum'
}


class EventNameEnum(Enum):
    register: str = "RegisterEvent"
    investor: str = "Investor"
    buy_token: str = "BuyToken"
    withdraw: str = "Withdraw"


class RoundEnum(Enum):
    PUBLICSALE = 'PUBLICSALE'
    PRESALE = 'PRESALE'
