from enum import Enum


class OrderStatus(Enum):
    Completed = 'Hoàn thành'
    InComplete = 'Chưa hoàn thành'


class CallbackStatus(Enum):
    Successfully = "Successfully"
    UnSuccessfully = "UnSuccessfully"
