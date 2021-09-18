import datetime as dt
import pandas as pd
from tasks.customer_info_1 import CustomerInfo
from datetime import timedelta

class ExpectedCustomerBehavior:
    """
    Calculate the expected behavior of a customer
    ---
    Attributes:
        - IPT_FACTOR                    - the factor to define the timeframe for the expected behavior
        - transactions                  - contains the customer transaction data
        - last_date                     - the last (possible) available date in the **data set**

        - last_transaction_date         - The time until which the data will be considered to calculate
                                          the expected behavior of the **customer**
        - expected_daily_rev            - Calculated after slicing the transactions until the <last_transaction_date>
                                          The expected daily rev is either
                                            a) the median value
                                            b) the .5 quantile of a fitted probability distribution function

        - expected_rev_until_last_date  - take the revenue from <last_transaction_date> onward
                                          and subtract for every day until <last_date> the daily_rev_hat

        - rev_made                      - the revenue the customer has made in the timeframe between
                                          ipt*IPT_FACTOR
    """
    IPT_FACTOR = 3
    transactions: pd.DataFrame
    last_date: dt.date

    last_transaction_date: dt.date
    expected_daily_rev: float
    expected_rev_until_last_date: int
    rev_made: int

    def __init__(self,
                 transactions: pd.DataFrame,
                 last_date: dt.date):
        self.transactions = transactions
        df = transactions
        self.last_date = last_date


        # ########################
        # Your code goes here...
        # ########################


        self.customer = CustomerInfo(transactions)

        # Create the ipt_product by multiplying the ipt from 1) with IPT_FACTOR
        self.ipt_product = self.customer.ipt * ExpectedCustomerBehavior.IPT_FACTOR

        # Slice the transactions from first = (self.last_date - ipt_product * 2),  until second = (self.last_date - ipt_product)

        first = self.last_date - timedelta(self.ipt_product * 2)
        second = self.last_date - timedelta(self.ipt_product)

        # converting date to datetime for comparison
        first = dt.datetime.combine(first, dt.datetime.min.time())
        second = dt.datetime.combine(second, dt.datetime.min.time())

        transaction_bw_dates = transactions[(df['transaction_date'] >= first) & (df['transaction_date'] <= second)]

        # From sliced transaction, select the transaction date which has the highest revenue
        if len(transaction_bw_dates) != 0:
            # if 2 or more max_revenue then select last one.
            self.last_transaction_date = transaction_bw_dates['transaction_date'][
                transaction_bw_dates['revenue'] == transaction_bw_dates['revenue'].max()][-1]

            self.last_transaction_date = self.last_transaction_date.date()
        # If there are no transactions in slice, select last possible date before, second_date = (self.last_date - ipt_product).
        else:
            self.last_transaction_date = transactions['transaction_date'][(df['transaction_date'] < second)].tail(1).iloc[0].date()

        # convert last transaction date to datetime for comparison
        last_transaction_date_time = dt.datetime.combine(self.last_transaction_date, dt.datetime.min.time())

        # Extract transaction until last_transaction date
        transactions_until_last_transaction_date = df[df['transaction_date'] <= last_transaction_date_time]
        diff_bw_transaction = (transactions_until_last_transaction_date - transactions_until_last_transaction_date.shift(1))


        # Calculate the expected revenue until the last_date by multiplying the expected daily revenue by the remaining days
        # (from last_transaction_date until last_date)

        # calculate difference in days
        days = diff_bw_transaction['transaction_date'].astype('timedelta64[D]').shift(-1)

        revenue = transactions_until_last_transaction_date['revenue']

        #  Expected daily revenue and get median
        self.expected_daily_rev = (revenue / days).median()
        self.expected_rev_until_last_date = round((self.last_date - self.last_transaction_date).days * self.expected_daily_rev)

        # convert last_transaction_date to datetime for comparison
        last_transaction_date_time = dt.datetime.combine(self.last_transaction_date, dt.datetime.min.time())

        # Calculate the rev_made (the revenue that was really made) after the last_transaction_date
        self.rev_made = transactions['revenue'][(df['transaction_date'] >= last_transaction_date_time)].sum()

