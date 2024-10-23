from src.command.base_command import Command
import pandas as pd

class FindTopKEarnerByCommissionPeriod(Command):
    """
    Find the top K earners based on commission for a given period.
    """
    @classmethod
    def get_name(cls) -> str:
        return 'find_top_k_earner'

    @classmethod
    def get_args(cls) -> list[dict]:
        return \
            [
                {
                    'name': 'k',
                    'type': 'int',
                    'required': True
                },
                {
                    'name': 'period',
                    'type': 'str',
                    'required': True
                }
            ]

    @classmethod
    def get_help_info(cls) -> str:
        return ("Find the top K earners based on commission for a given period, "
                "first parameter is the number of earners to return, type int, "
                "second parameter is the period of time, type str")

    @classmethod
    def get_parameters(cls, args) -> dict:
        """
        Extract and validate parameters from input args.
        :param args:
        :return:
        """
        k = args['k']
        if k <= 0:
            raise ValueError("k must be greater than 0.")
        period = args['period']
        if not period:
            raise ValueError("period must be provided.")
        return {'k': k, 'period': period}

    def execute(self, dataframe, **kwargs):
        """
        Find the top k earners based on their total commission for a given period
        :param dataframe:
        :return:
        """
        k = kwargs['k']
        period = kwargs['period']
        dataframe['Commission_Period'] = pd.to_datetime(dataframe['Commission_Period'], errors='coerce')
        filtered_df = dataframe[dataframe['Commission_Period'].dt.strftime('%Y-%m') == period]

        top_earners = filtered_df.groupby('Earner_Name').agg(
            {'Commission_Amount': 'sum'}
        ).sort_values('Commission_Amount', ascending=False).head(k)[['Commission_Amount']]

        print(f'Top {k} earners based on total commission for period {period}:')
        print(top_earners)
        return top_earners
