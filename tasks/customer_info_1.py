import numpy as np
import pandas as pd

MIN_PURCHASES = 6


class CustomerInfo:
    """
    Attributes:
        - transactions: Contains the transaction history of a customer
        - ipt           - The median interpurchase time or time between two transactions
    """
    transactions: pd.DataFrame
    ipt: float

    def __init__(self, transactions: pd.DataFrame):
        self.transactions = transactions.sort_values(by='transaction_date')
        # for short hand
        df = transactions

        # Convert string date to datetime
        df['transaction_date'] = df['transaction_date'].astype('datetime64[ns]')

        # calculate difference within each next transaction date, convert them to days and take median
        median_ipt = (df['transaction_date'] - df['transaction_date'].shift(1)).astype('timedelta64[D]').median()

        self.ipt = median_ipt

