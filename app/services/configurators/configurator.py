"""Parent class of configurators."""

__all__ = ["Configurator"]

import os
import logging
from abc import ABC, abstractmethod


class Configurator(ABC):
    """Configurator of a specific language and framework.

    Args:
        ABC (_type_): Abstract class.
    """

    def __init__(self, attributes: dict[str, any]) -> None:
        """Create a Configurator.

        Args:
            attributes (dict[str, any]): Configurator attributes.
        Raises:
            KeyError: When missing fields.
            NotADirectoryError: When path does not exist.
        """

        self._validate(attributes)

        self._path: str = attributes["path"]
        if not os.path.isdir(self._path):
            error = f'Path "{self._path}" does not exist.'
            logging.error(error)
            raise NotADirectoryError(error)

    def _validate(self, attributes: dict[str, any]) -> None:
        """Validate configuration attributes. Throw exceptions when not validated.

        Args:
            attributes (dict[str, any]): attributes in json.
        Raises:
            KeyError: When missing fields.
        """

        keys = ["path"]

        for key in keys:
            if key not in attributes:
                error = f'Missing field "{key}".'
                logging.error(error)
                raise KeyError(error)

    @classmethod
    def get_configurations(cls) -> dict[str, any]:
        """Get supported configuration methods and attributes of those method.

        Returns:
            dict[str, any]: Json of supported configuration methods and attributes of those method.
        """
        configurations = {
            ".gitignore": None,
        }
        return configurations

    @classmethod
    def get_initialized_configurations(cls, path: str) -> list[str]:
        """Get a list of configuration files which this project has initialized.

        Args:
            path (str): Path of the project.

        Raises:
            NotADirectoryError: When path does not exist.

        Returns:
            list[str]: A list of configuration files which this project has initialized.
        """

        if not os.path.isdir(path):
            error = f'Path "{path}" does not exist.'
            logging.error(error)
            raise NotADirectoryError(error)

        keys = cls.get_configurations().keys()
        initialized = []
        for key in keys:
            if os.path.isfile(os.path.join(path, key)):
                initialized.append(key)
        return initialized

    def get_serialize_data(self) -> dict[str, any]:
        """Get data to be serialized to the yaml.

        Returns:
            dict[str, any]: Data to be serialized to the yaml.
        """
        return {}

    def _get_general_gitignore(self) -> str:
        """Get general gitignore content.

        Returns:
            str: General gitignore content.
        """
        files = [".DS_Store", "env/", ".env", ".vscode"]
        return "\n".join(files)

    def _build_gitignore(self) -> None:
        """Create a .gitignore file under project folder."""

        with open(
            os.path.join(self._path, ".gitignore"), "w", encoding="utf-8"
        ) as file:
            file.write(self._get_general_gitignore())

    @abstractmethod
    def build_configurations(self) -> None:
        """Build configurations for the project in local storage."""
        return NotImplemented
