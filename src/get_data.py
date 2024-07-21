import os


class GetData:
    def __init__(self, folder_path: str) -> None:
        self.all_data = self.read_all_data(folder_path)

    def read_all_data(self, folder_path: str) -> list:
        """
        Read all data from the csv files.

        :param folder_path: Relative path to the folder which contains the csv files.
        :return: List representing all lines from all files.
        """
        files = os.listdir(folder_path)
        content = []
        files = [one_file for one_file in files if one_file.endswith('.csv')]
        for one_file in files:
            with open(f'data/{one_file}', encoding="utf-8-sig") as f:
                lines = f.readlines()
                [content.append(one_line) for one_line in lines]
        return content

    def get_deposits(self) -> list:
        """
        Get all deposits and withdrawals from the data.

        :return: List representing all lines that contain the withdrawals and desposits amounts.
        """
        all_deposits = []
        for one_line in self.all_data:
            if one_line.startswith('Deposits & Withdrawals,Data,Total'):
                all_deposits.append(float(one_line.strip()[36:]))

        return all_deposits

    def sum_deposits(self) -> float:
        """
        Get the sum of all of the deposits.

        :return: Return the value of all deposits made to the account.
        """
        all_deposits = self.get_deposits()
        sum_deposits = 0
        for one_deposit in all_deposits:
            if one_deposit > 0:
                sum_deposits += one_deposit
        return sum_deposits

    def sum_withdrawals(self) -> float:
        """
        Get the sum of all withdrawals.

        :return: Value for all withdrawals.
        """
        all_transasctions = self.get_deposits()
        sum_withdrawals = 0
        for one_value in all_transasctions:
            if one_value < 0:
                sum_withdrawals += float(abs(one_value))
        return sum_withdrawals

    def last_nav(self) -> float:
        """
        Get the last value for NAV.

        :return: Last NAV.
        """
        for one_line in self.all_data[::-1]:
            if one_line.startswith('Change in NAV,Data,Ending Value,'):
                return float(one_line.strip()[32:])
        else:
            return 0
