from src.command.base_command import Command

class FindTopKCarrier(Command):
    """
    Find the top K carriers based on commission.
    """
    @classmethod
    def get_name(cls) -> str:
        return 'find_top_k_carrier'

    @classmethod
    def get_args(cls) -> list[dict]:
        return \
            [
                {
                    'name': 'k',
                    'type': 'int',
                    'required': True
                }
            ]

    @classmethod
    def get_help_info(cls) -> str:
        return "Find the top K carriers based on commission, first parameter is the number of plans to return, type int"

    def __init__(self, k: int):
        self.k = k

    def execute(self, dataframe):
        """
        Find the top k carriers based on their total commission
        :param dataframe:
        :return:
        """
        k = self.k
        top_carriers = dataframe.groupby('Carrier_Name').agg(
            {'Commission_Amount': 'sum'}
        ).sort_values('Commission_Amount', ascending=False).head(k)[['Commission_Amount']]
        print(f'Top {k} carriers based on total commission:')
        print(top_carriers)

        return top_carriers