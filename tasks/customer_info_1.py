import numpy as np
import pandas as pd

MIN_PURCHASES = 6


class CustomerInfo:
    """
    Attributes:
        - transactions: Contains the transaction history of a customer
        (TODO 1.1)
        - ipt           - The median interpurchase time or time between two transactions
    """
    transactions: pd.DataFrame
    # TODO 1.1
    ipt: float

    def __init__(self, transactions: pd.DataFrame):
        self.transactions = transactions
        self.ipt = np.nan
