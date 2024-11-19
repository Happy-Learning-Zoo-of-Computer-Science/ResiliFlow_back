"""
Serialize and deserialize project information.
"""

__all__ = ["ProjectSerializor"]

import os
import logging

import yaml


class ProjectSerializor:
    """Serialize and deserialize project information."""

    __CONFIGURATION_FOLDER_NAME = ".hlzcs"
    __PROJECT_ATTRIBUTE_FILE_NAME = "project_attribute.yaml"
    __SUPPORTED_LANGUAGE = tuple("Python")

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
        return cls.__SUPPORTED_LANGUAGE

    @classmethod
    def serialize(cls, path: str, project_attributes: dict[str, str]) -> None:
        """Serialize the project attributes to a yaml file.

        Args:
            path (str): Path of the project folder.
            project_attributes (dict[str, str]): Dictionary of project attributes.
        Raises:
            NotADirectoryError: When the path doesn' exist.
        """

        # Check path.
        folder_path = os.path.join(path, cls.__CONFIGURATION_FOLDER_NAME)
        if not os.path.isdir(folder_path):
            raise_not_a_directory(folder_path)

        # TODO Validate configurations.

        # Dump to yaml.
        with open(
            os.path.join(folder_path, cls.__PROJECT_ATTRIBUTE_FILE_NAME),
            "w",
            encoding="utf-8",
        ) as file:
            yaml.dump(project_attributes, file)

    @classmethod
    def deserialize(cls, path: str) -> dict[str, str]:
        """Read project attributes from the configuration file.

        Args:
            path (str): Path of the project.

        Returns:
            dict[str, str]: Project attributes.
        Raises:
            FileNotFoundError: When the attribute file doesn't exist.
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

        # TODO Validate attributes.

        return attributes


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
