from src.command.base_command import Command


class ListAllCarriersCommand(Command):
    """
    List all carriers.
    """
    @classmethod
    def get_name(cls) -> str:
        return 'list_carriers'

    @classmethod
    def get_args(cls) -> list[dict]:
        return []

    @classmethod
    def get_help_info(cls) -> str:
        return "List all carriers"


    def execute(self, dataframe):
        carriers = dataframe['Carrier_Name'].unique()
        print(f'All carriers:')
        print(carriers)
        return carriers