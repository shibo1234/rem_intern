import os
from src.command import Command

class ExportCsv(Command):
    """
    Export the dataframe to a CSV file.
    """
    @classmethod
    def get_name(cls) -> str:
        return 'export_csv'

    @classmethod
    def get_args(cls) -> list[dict]:
        return \
        [
            {
                'name': 'path',
                'type': 'str',
                'required': True
            }
        ]

    @classmethod
    def get_help_info(cls) -> str:
        return "Export the normalized CSV to the specified path."

    def execute(self, dataframe, **kwargs):
        """
        Export the dataframe to a CSV file.
        :param dataframe: The dataframe to export.
        :param kwargs: Additional arguments (in this case, the path).
        :return:
        """
        path = kwargs.get('path')
        if os.path.isdir(path):
            path = os.path.join(path, "exported_data.csv")
            print(f"Provided path is a directory. Saving as: {path}")

        dir_path = os.path.dirname(path)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Directory '{dir_path}' created.")

        dataframe.to_csv(path, index=False)
        print(f"Dataframe exported to {path}")
        return

    @classmethod
    def get_parameters(cls, command_args):
        path = command_args.get('path')
        if not path:
            raise ValueError("You must provide a path to export the CSV.")
        return {'path': path}
