"""Test services.configurators.configurator"""

import os
import shutil
import unittest

from app.services.configurators.configurator import Configurator


class TestConfigurator(Configurator):
    """Test class."""

    def build_configurations(self) -> None:
        pass


class MyTestCase(unittest.TestCase):
    """Test class."""

    def setUp(self) -> None:
        # Create a folder.
        self.__folder = "test_folder"
        os.mkdir(self.__folder)
        self.__folder = os.path.join(os.path.curdir, self.__folder)
        self.__attributes = {"path": self.__folder}
        self.__configurator = TestConfigurator(self.__attributes)

    def tearDown(self) -> None:
        # Delete the folder.
        shutil.rmtree(self.__folder)

    def test＿constructor(self) -> None:
        """Test constructor."""

        # Incorrect path.
        self.__attributes["path"] = self.__attributes["path"] + "a"
        with self.assertRaises(NotADirectoryError):
            self.__configurator = TestConfigurator(self.__attributes)

        # No path.
        self.__attributes.pop("path")
        with self.assertRaises(KeyError):
            self.__configurator = TestConfigurator(self.__attributes)

    def test_get_configurations(self) -> None:
        """Test get_configurations()"""

        self.assertEqual(
            {".gitignore": None}, TestConfigurator.get_configurations()
        )

    def test_get_initialized_configurations(self) -> None:
        """Test get_initialized_configurations()"""

        self.assertEqual(
            [], TestConfigurator.get_initialized_configurations(self.__folder)
        )

        self.__configurator._build_gitignore()
        self.assertEqual(
            [".gitignore"],
            TestConfigurator.get_initialized_configurations(self.__folder),
        )

        with self.assertRaises(NotADirectoryError):
            TestConfigurator.get_initialized_configurations(
                self.__folder + "A"
            )

    def test_get_serialize_data(self) -> None:
        """Test get_serialize_data()"""

        self.assertEqual({}, self.__configurator.get_serialize_data())

    def test_get_general_gitignore(self) -> None:
        """Test get_general_gitignore()"""

        self.assertEqual(
            ".DS_Store\nenv/\n.env\n.vscode",
            self.__configurator._get_general_gitignore(),
        )


if __name__ == "__main__":
    unittest.main()
