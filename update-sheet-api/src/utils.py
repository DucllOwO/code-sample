import logging
import random
import string
import re
import os
from datetime import datetime
from databases.interfaces import Record
from dateutil.relativedelta import relativedelta
from calendar import monthrange
from sqlalchemy import inspect

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

logger = logging.getLogger(__name__)
ALPHA_NUM = string.ascii_letters + string.digits


def generate_random_alphanum(length: int = 20) -> str:
    return "".join(random.choices(ALPHA_NUM, k=length))


def get_spreadsheet_id(url):
    '''
    # Example usage
    url = "https://docs.google.com/spreadsheets/d/1NZiPRbtzam8NXsTRD3HIJv0hROndlIdgeLcyUwLfk-w/edit?pli=1&gid=242522757#gid=242522757"
    spreadsheet_id = get_spreadsheet_id(url)
    print(spreadsheet_id)  # Output: 1NZiPRbtzam8NXsTRD3HIJv0hROndlIdgeLcyUwLfk-w
'''
    # Regular expression pattern to match the spreadsheet ID
    pattern = r"/spreadsheets/d/([a-zA-Z0-9-_]+)"

    # Search for the pattern in the URL
    match = re.search(pattern, url)

    # If a match is found, return the spreadsheet ID
    if match:
        return match.group(1)
    else:
        return None


def convert_vn_phone_to_international(phone_number):
    '''
    Converts Vietnamese phone numbers to international format.

    Examples:
    "0969362553" -> "+84969362553"
    "84969362553" -> "+84969362553"
    "+84969362553" -> "+84969362553"
    "969362553" -> "+84969362553"
    '''
    # Remove any non-digit characters except '+'
    cleaned_number = ''.join(
        char for char in phone_number if char.isdigit() or char == '+')

    # If the number already starts with '+84', return it as is
    if cleaned_number.startswith('+84'):
        return cleaned_number

    # If the number starts with '84', add a '+'
    if cleaned_number.startswith('84'):
        return '+' + cleaned_number

    # If the number starts with '0', replace it with '+84'
    if cleaned_number.startswith('0'):
        return '+84' + cleaned_number[1:]

    # If the number doesn't start with '0', '84', or '+84', assume it's a local number without the leading '0'
    return '+84' + cleaned_number


def build_spreadsheet_url(spreadsheet_id: str):
    return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
