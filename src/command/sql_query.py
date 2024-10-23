from src.command.base_command import Command
import pandasql as psql


class SqlQuery(Command):
    """
    Execute a SQL query.
    """

    @classmethod
    def get_name(cls) -> str:
        return 'sql_query'

    @classmethod
    def get_args(cls) -> list[dict]:
        return \
        [
            {
                'name': 'query',
                'type': 'str',
                'required': True,
                'help': 'SQL query to execute'
            }
        ]

    @classmethod
    def get_help_info(cls) -> str:
        return "Execute a SQL query on the dataframe"


    def __init__(self, query: str):
        self.query = query

    def execute(self, dataframe):
        """
        Execute the SQL query
        :param dataframe:
        :return:
        """
        print(f"Executing query: {self.query}")
        print(psql.sqldf(self.query, {"df": dataframe}))
        return psql.sqldf(self.query, {"df": dataframe})