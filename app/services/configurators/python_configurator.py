"""Python configurator of various framework."""

__all__ = ["PythonConfigurator"]

import os
import logging

from app.services.configurators.configurator import Configurator


class PythonConfigurator(Configurator):
    """Configurator of Python with no specific framework.

    Args:
        Configurator (_type_): Parent class.
    """

    # Class specific configurations.
    __SPECIFIC_CONFIGURATIONS = {}

    def __init__(self, attributes: dict[str, any]) -> None:
        """Create a Python Configurator with no specific framework.

        Args:
            attributes (dict[str, any]): Configurator attributes.
        Raises:
            KeyError: When missing fields.
            NotADirectoryError: When path does not exist.
        """

        super().__init__(attributes)
        self._validate(attributes)
        self._language = "Python"
        self._attributes = attributes.copy()

    def _validate(self, attributes: dict[str:any]) -> None:
        """Validate configuration attributes. Throw exceptions when not validated.

        Args:
            attributes (dict[str, any]): attributes in json.
        Raises:
            KeyError: When missing fields.
            ValueError: When attribute value is not supported.
        """

        keys = []

        for key in keys:
            if key not in attributes:
                error = f'Missing field "{key}".'
                logging.error(error)
                raise KeyError(error)

        if attributes["language"] != "Python":
            error = "Language of Python Configurator has to be Python. "
            error += f'Got "{attributes["language"]}".'
            logging.error(error)
            raise ValueError(error)

    @classmethod
    def get_configurations(cls) -> dict[str, any]:
        """Get supported configuration methods and attributes of those method.

        Returns:
            dict[str, any]: Json of supported configuration methods and attributes of those method.
        """
        configurations = Configurator.get_configurations()
        # Append class specific configurations here.
        for key, value in cls.__SPECIFIC_CONFIGURATIONS.items():
            configurations[key] = value
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

        initialized = Configurator.get_initialized_configurations(path)
        keys = cls.__SPECIFIC_CONFIGURATIONS.keys()
        for key in keys:
            if os.path.isfile(os.path.join(path, key)):
                initialized.append(key)
        return initialized

    def get_serialize_data(self) -> dict[str, any]:
        """Get data to be serialized to the yaml.

        Returns:
            dict[str, any]: Data to be serialized to the yaml.
        """

        data = super().get_serialize_data()
        data["language"] = "Python"
        return data

    def _build_gitignore(self) -> None:
        """Create a .gitignore file under project folder."""

        content = super()._get_general_gitignore()
        files = [content, ".venv/", "__pycache__/", "*.py[cod]", "*.log"]
        content = "\n".join(files)
        with open(
            os.path.join(self._path, ".gitignore"), "w", encoding="utf-8"
        ) as file:
            file.write(content)

    def build_configurations(self) -> None:
        """Build configurations for the project in local storage."""

        call = {".gitignore": self._build_gitignore}
        for key, value in self._attributes.items():
            if key not in call:
                continue
            if value is not None:
                call[key](value)
            else:
                call[key]()
