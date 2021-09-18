from enum import IntEnum
import datetime as dt

import pandas as pd

from tasks.expected_customer_behavior_2 import ExpectedCustomerBehavior


class AtRisk(IntEnum):
    """
    Use this class to provide the answer for at_risk.
    It will make sure, that the answer is given and you haven't made an error in the string
    """
    YES = 2
    MAYBE = 1
    NO = 0
    UNKNOWN = -99999

class Customer:
    """
    Is the customer at risk? To evaluate that you have to:
        1. Calculate the mean IPT of the customer with the CustomerInfo class
        2. Calculate the expected behavior for a variable timeframe
        3. Compare the expected behavior with the real behavior

    A customer will have different risk statuses depending on
    the revenue that was made and the expected revenue.
    The risk percentages are inside RISK_PERCENTAGE
    ---
    Attributes:
        - RISK_PERCENTAGES          - Defines the percentage bounds for the different risk statuses
        - transactions              - contains the customer transaction data
        - last_date                 - the last (possible) available date in the data set.
                                      Not to be confused with

        - at_risk                   - the class of the customer
    """
    RISK_PERCENTAGES = {
        AtRisk.YES: {
           'min': -999999,
           'max': .35
        },
        AtRisk.MAYBE: {
            'min': .35,
            'max': .65
        },
        AtRisk.NO: {
            'min': .65,
            'max': 999999
        }
    }


    transactions: pd.DataFrame
    at_risk: AtRisk

    def __init__(self,
                 transactions: pd.DataFrame,
                 last_date: dt.date):
        self.transactions = transactions
        self.last_date = last_date
        self.at_risk = AtRisk.NO
        expected_behavior = ExpectedCustomerBehavior(transactions=transactions, last_date=dt.date(2021, 7, 16))

        # quotient between the revenue_made and the expected_rev
        self.quotient = round(expected_behavior.rev_made / expected_behavior.expected_rev_until_last_date, 3)

        # check which risk class the Customer revenue quotient belongs to
        for key, value in Customer.RISK_PERCENTAGES.items():
            if value['min'] < self.quotient < value['max']:
                self.at_risk = key