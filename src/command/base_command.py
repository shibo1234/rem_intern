from abc import abstractmethod, ABC
from .command_meta import CommandMeta

class Command(metaclass=CommandMeta):
    """
    Base command class
    """
    @classmethod
    @abstractmethod
    def get_name(cls) -> str:
        """
        Get the name of the command
        :return:
        """
        raise NotImplementedError("Each command must implement a get_name method.")

    @classmethod
    @abstractmethod
    def get_args(cls) -> list[dict]:
        """
        Get the arguments of the command
        :return:
        """
        raise NotImplementedError("Each command must implement a get_args method.")

    @classmethod
    @abstractmethod
    def get_help_info(cls) -> str:
        """
        Get the help information of the command
        :return:
        """
        raise NotImplementedError("Each command must implement a get_args method.")

    @abstractmethod
    def execute(self, dataframe):
        """
        Execute the command
        :param dataframe:
        :return:
        """
        raise NotImplementedError("Each command must implement an execute method.")

