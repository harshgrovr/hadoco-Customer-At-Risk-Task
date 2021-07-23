import datetime as dt

import pandas as pd
import numpy as np


# TODO 2
class ExpectedCustomerBehavior:
    """
    Calculate the expected behavior of a customer
    ---
    Attributes:
        - IPT_FACTOR                    - the factor to define the timeframe for the expected behavior
        - transactions                  - contains the customer transaction data
        - last_date                     - the last (possible) available date in the **data set**

        (TODO 2.1)
        - last_transaction_date         - The time until which the data will be considered to calculate
                                          the expected behavior of the **customer**
        (TODO 2.2)
        - expected_daily_rev            - Calculated after slicicng the transactions until the <last_transaction_date>
                                          The expected daily rev is either
                                            a) the median value
                                            b) the .5 quantile of a fitted probability distribution function

        (TODO: 2.3)
        - expected_rev_until_last_date  - take the revenue from <last_transaction_date> onward
                                          and subtract for every day until <last_date> the daily_rev_hat

        (TODO: 2.4)
        - rev_made                      - the revenue the customer has made in the timeframe between
                                          ipt*IPT_FACTOR
    """
    IPT_FACTOR = 3
    transactions: pd.DataFrame
    last_date: dt.date

    # TODO 2.2:
    last_transaction_date: dt.date
    # TODO 2.1:
    expected_daily_rev: float
    # TODO 2.3:
    expected_rev_until_last_date: int
    # TODO 2.4
    rev_made: int

    def __init__(self,
                 transactions: pd.DataFrame,
                 last_date: dt.date):
        self.transactions = transactions
        self.last_date = last_date

        # ########################
        # Your code goes here...
        # ########################
        self.last_transaction_date = dt.date(2000, 1, 1)
        self.expected_daily_rev = np.nan
        self.expected_rev_until_last_date = -999
        self.rev_made = -999