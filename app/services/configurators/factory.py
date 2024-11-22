"""Create a configurator from factory."""

__all__ = ["ConfiguratorFactory"]

import logging

from app.services.configurators.configurator import Configurator
from app.services.configurators.python_configurator import (
    PythonConfigurator,
)


class ConfiguratorFactory:
    """Factory that creates Configurator based on attributes."""

    __CONFIGURATOR = {"Python": PythonConfigurator}

    @classmethod
    def get_configurator(cls, attributes: dict[str, any]) -> Configurator:
        """Get the Configurator of specifc language and framework.
        Language should be included in the attributes.

        Args:
            attributes (dict[str, any]): attributes in json.
        Returns:
            Configurator: A configurator project.
        Raises:
            KeyError: When missing fields.
            ValueError: When language or framework not supported.
        """

        if "language" not in attributes:
            error = "Need language information to get a Configurator."
            logging.error(error)
            raise KeyError(error)

        language = attributes["language"]
        if "framework" in attributes:
            language += "@" + attributes["framework"]

        if language not in cls.__CONFIGURATOR:
            error = f'Language and framework "{language}" are not supported.'
            logging.error(error)
            raise ValueError(error)

        return cls.__CONFIGURATOR[language](attributes)

    @classmethod
    def get_supported_languages(cls) -> tuple[str]:
        """Get a tuple of languages supported by our application.

        Returns:
            tuple[str]: A tuple of suppoerted languages.
        """

        languages = set()
        for key in cls.__CONFIGURATOR:
            languages.add(key.split("@")[0])

        return tuple(languages)

    @classmethod
    def get_supported_frameworks(cls, language: str) -> tuple[str]:
        """Get a tuple of templates of a language supported by our application.

        Args:
            language (str): A programming language.

        Returns:
            tuple[str]: A tuple of supported frameworks.
        """

        frameworks = set()
        for key in cls.__CONFIGURATOR:
            if language in key and language != key:
                frameworks.add(key.split("@")[1])

        return tuple(frameworks)

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

        if framework is not None:
            language += f"@{framework}"

        if language not in cls.__CONFIGURATOR:
            return {}

        return cls.__CONFIGURATOR[language].get_configurations()

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

        if framework is not None:
            language += f"@{framework}"

        if language not in cls.__CONFIGURATOR:
            return {}

        return cls.__CONFIGURATOR[language].get_initialized_configurations(
            path
        )
