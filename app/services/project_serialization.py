"""
Serialize and deserialize project information.
"""

__all__ = ["ProjectSerializor"]

import os
import logging

import yaml

from app.services.configurators.factory import ConfiguratorFactory


class ProjectSerializor:
    """Serialize and deserialize project information."""

    __CONFIGURATION_FOLDER_NAME = ".hlzcs"
    __PROJECT_ATTRIBUTE_FILE_NAME = "project_attributes.yaml"

    @classmethod
    def is_initialized(cls, path: str) -> bool:
        """Check is the project initialized.

        Args:
            path (str): Project path.

        Returns:
            bool: Is the project initialized.
        """

        return os.path.isdir(
            os.path.join(path, cls.__CONFIGURATION_FOLDER_NAME)
        )

    @classmethod
    def create_configuration_folder(cls, path: str) -> None:
        """Create a folder to put our configuration files.

        Args:
            path (str): Path of the project folder.
        Raises:
            NotADirectoryError: When the path doesn't exist.
        """

        # Check the path is a folder.
        if not os.path.isdir(path):
            raise_not_a_directory(path)

        # Check the new folder is exist.
        configuration_folder_path = os.path.join(
            path, cls.__CONFIGURATION_FOLDER_NAME
        )
        if os.path.isdir(configuration_folder_path):
            return

        # Create an empty folder.
        os.mkdir(configuration_folder_path)

    @classmethod
    def get_supported_langauges(cls) -> tuple[str]:
        """Get a tuple of languages supported by our application.

        Returns:
            tuple[str]: A tuple of suppoerted languages.
        """
        return ConfiguratorFactory.get_supported_languages()

    @classmethod
    def get_supported_frameworks(cls, language: str) -> tuple[str]:
        """Get a tuple of templates of a language supported by our application.

        Args:
            language (str): A programming language.

        Returns:
            tuple[str]: A tuple of supported frameworks.
        """
        return ConfiguratorFactory.get_supported_frameworks(language)

    @classmethod
    def get_configurations(
        cls, language: str, framework: str = None
    ) -> dict[str, any]:
        """Get supported configuration methods and attributes of those method.

        Args:
            language (str): A programming language.
            framework (str): A programming language framework.
        Returns:
            dict[str, any]: Json of supported configuration methods and attributes of those method.
        """
        return ConfiguratorFactory.get_configurations(language, framework)

    @classmethod
    def get_initialized_configurations(
        cls, path: str, language: str, framework: str = None
    ) -> list[str]:
        """Get a list of configuration files which this project has initialized.

        Args:
            path (str): Path of the project.
            language: A coding language.
            framework: A coding language framework.

        Raises:
            NotADirectoryError: When path does not exist.

        Returns:
            list[str]: A list of configuration files which this project has initialized.
        """
        return ConfiguratorFactory.get_initialized_configurations(
            path, language, framework
        )

    @classmethod
    def serialize(cls, path: str, attributes: dict[str, str]) -> None:
        """Serialize the project attributes to a yaml file.

        Args:
            path (str): Path of the project folder.
            attributes (dict[str, str]): Dictionary of project attributes.
        Raises:
            NotADirectoryError: When the path doesn' exist.
            KeyError: When missing any field.
            ValueError: When language isn't supported.
        """

        # Check path.
        folder_path = os.path.join(path, cls.__CONFIGURATION_FOLDER_NAME)
        if not os.path.isdir(folder_path):
            raise_not_a_directory(folder_path)

        # Dump to yaml.
        with open(
            os.path.join(folder_path, cls.__PROJECT_ATTRIBUTE_FILE_NAME),
            "w",
            encoding="utf-8",
        ) as file:
            yaml.dump(attributes, file)

    @classmethod
    def deserialize(cls, path: str) -> dict[str, str]:
        """Read project attributes from the configuration file.

        Args:
            path (str): Path of the project.

        Returns:
            dict[str, str]: Project attributes.
        Raises:
            FileNotFoundError: When the attribute file doesn't exist.
            KeyError: When missing any field.
            ValueError: When language isn't supported.
        """

        # Check path.
        file_path = os.path.join(
            path,
            cls.__CONFIGURATION_FOLDER_NAME,
            cls.__PROJECT_ATTRIBUTE_FILE_NAME,
        )
        if not os.path.isfile(file_path):
            error = f"File {file_path} does not exist."
            logging.error(error)
            raise FileNotFoundError(error)

        # Read from path.
        with open(file_path, "r", encoding="utf=8") as file:
            attributes = yaml.safe_load(file)

        # Validate attributes.
        attributes["path"] = path
        ConfiguratorFactory.get_configurator(attributes)

        return attributes

    @classmethod
    def create_project(cls, data: dict[str, str]) -> None:
        """Create a configuration and serialize project attributes.

        Args:
            data (dict[str, str]): Data from the request.

        Raises:
            KeyError: When missing any field.
            NotADirectoryError: When the path doesn't exist.
            ValueError: When language isn't supported.
        """

        # Get attributes.
        if "path" not in data:
            error = 'Missing field "path".'
            logging.error(error)
            raise KeyError(error)

        path = data["path"]
        cls.create_configuration_folder(path)
        configurator = ConfiguratorFactory.get_configurator(data)
        configurator.build_configurations()
        cls.serialize(path, configurator.get_serialize_data())


def raise_not_a_directory(path: str) -> None:
    """Log and raise a NotADirectoryError.

    Args:
        path (str): Path that doesn't exist.

    Raises:
        NotADirectoryError: return value.
    """
    error = f'Path "{path}" does not exist.'
    logging.error(error)
    raise NotADirectoryError(error)
