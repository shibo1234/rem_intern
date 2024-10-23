from src.command.base_command import Command


class FindTopKPlan(Command):
    """
    Find the top K plans based on commission.
    """
    @classmethod
    def get_name(cls) -> str:
        return 'find_top_k_plan'

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
        return "Find the top K plans based on commission, first parameter is the number of plans to return, type int"


    def __init__(self, k: int):
        self.k = k

    def execute(self, dataframe):
        """
        Find the top k plans based on their total commission
        :param dataframe:
        :return:
        """
        k = self.k
        top_plans = dataframe.groupby('Plan_Name').agg(
            {'Commission_Amount': 'sum'}
        ).sort_values('Commission_Amount', ascending=False).head(k)[['Commission_Amount']]
        print(f'Top {k} plans based on total commission:')
        print(top_plans)
        return top_plans