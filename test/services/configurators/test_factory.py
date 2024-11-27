"""Test"""

import os
import shutil
import unittest

from app.services.configurators.factory import ConfiguratorFactory
from app.services.configurators.python_configurator import PythonConfigurator


class MyTestCase(unittest.TestCase):
    """Test"""

    def setUp(self):
        # Create a folder.
        self.__folder = "test_folder"
        os.mkdir(self.__folder)
        self.__folder = os.path.join(os.path.curdir, self.__folder)
        self.__attributes = {"path": self.__folder, "language": "Python"}

    def tearDown(self):
        shutil.rmtree(self.__folder)

    def test_get_configurator(self) -> None:
        """Test"""

        # Get python.
        configurator = ConfiguratorFactory.get_configurator(self.__attributes)
        self.assertIsInstance(configurator, PythonConfigurator)

        # Framework not supported.
        self.__attributes["framework"] = "Flask"
        with self.assertRaises(ValueError):
            ConfiguratorFactory.get_configurator(self.__attributes)

        # Missing field.
        self.__attributes.pop("language")
        self.__attributes.pop("framework")
        with self.assertRaises(KeyError):
            ConfiguratorFactory.get_configurator(self.__attributes)

    def test_get_supported_languages(self) -> None:
        """Test"""

        self.assertEqual(
            tuple(["Python"]), ConfiguratorFactory.get_supported_languages()
        )

    def test_get_supported_frameworks(self) -> None:
        """Test"""

        self.assertEqual(
            tuple(), ConfiguratorFactory.get_supported_frameworks("Python")
        )
        self.assertEqual(
            tuple(), ConfiguratorFactory.get_supported_frameworks("JavaScript")
        )

    def test_get_configurations(self) -> None:
        """Test"""

        self.assertEqual(
            PythonConfigurator.get_configurations(),
            ConfiguratorFactory.get_configurations("Python"),
        )
        self.assertEqual(
            {}, ConfiguratorFactory.get_configurations("Python", "Flask")
        )

    def test_get_initialized_configurations(self) -> None:
        """Test"""

        self.assertEqual(
            [],
            ConfiguratorFactory.get_initialized_configurations(
                self.__folder, "Python"
            ),
        )

        self.__attributes[".gitignore"] = None
        configurator = ConfiguratorFactory.get_configurator(self.__attributes)
        configurator.build_configurations()
        self.assertEqual(
            [".gitignore"],
            ConfiguratorFactory.get_initialized_configurations(
                self.__folder, "Python"
            ),
        )


if __name__ == "__main__":
    unittest.main()
