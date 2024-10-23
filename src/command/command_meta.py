from __future__ import annotations
from abc import ABCMeta
from typing import TYPE_CHECKING
from inspect import isabstract

class CommandMeta(ABCMeta):
    if TYPE_CHECKING:
        from .base_command import Command

    """
    Metaclass for command classes
    """

    _registry = {}

    def __new__(cls, name, bases, attrs):
        """
        Create a new command class
        :param name:
        :param bases:
        :param attrs:
        """
        command_class = super().__new__(cls, name, bases, attrs)
        if not isabstract(command_class):
            cls._registry[name] = command_class
            print(f"Registered command: {name}")
        return command_class

    def __class_getitem__(cls, item) -> type[Command]:
        """
        Get a command class by name
        :param item:
        :return:
        """
        return cls._registry[item]

    @classmethod
    def get_commands(mcs) -> dict[str, type[Command]]:
        """
        Get all registered commands
        :return:
        """
        return mcs._registry