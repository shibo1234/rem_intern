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


    @classmethod
    def get_parameters(cls, args) -> dict:
        """
        Extract and validate parameters from input args.
        This method can be extended for more complex parameter handling.
        """
        query = args['query']

        return {'query': query}

    def execute(self, dataframe, **kwargs):
        """
        Execute the SQL query
        :param dataframe:
        :return:
        """
        query = kwargs['query']
        print(f"Executing query: {query}")
        print(psql.sqldf(query, {"df": dataframe}))
        return psql.sqldf(query, {"df": dataframe})