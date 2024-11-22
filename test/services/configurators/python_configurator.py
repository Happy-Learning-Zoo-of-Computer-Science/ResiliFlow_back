"""Test services.configurators.python_configurator"""

import os
import shutil
import unittest

from app.services.configurators.python_configurator import PythonConfigurator


class MyTestCase(unittest.TestCase):
    """Test PythonConfigurator"""

    def setUp(self) -> None:
        # Create a folder.
        self.__folder = "test_folder"
        os.mkdir(self.__folder)
        self.__folder = os.path.join(os.path.curdir, self.__folder)
        self.__attributes = {"path": self.__folder, "language": "Python"}
        self.__configurator = PythonConfigurator(self.__attributes)

    def tearDown(self) -> None:
        shutil.rmtree(self.__folder)

    def test_constructor(self) -> None:
        """Test constructor"""

        self.__attributes["language"] = "python"
        with self.assertRaises(ValueError):
            self.__configurator = PythonConfigurator(self.__attributes)

    def test_get_configurations(self) -> None:
        """Test"""

        self.assertEqual(
            {".gitignore": None}, PythonConfigurator.get_configurations()
        )

    def test_get_initialized_configurations(self) -> None:
        """Test"""

        self.assertEqual(
            [],
            PythonConfigurator.get_initialized_configurations(self.__folder),
        )

        self.__configurator._build_gitignore()
        self.assertEqual(
            [".gitignore"],
            PythonConfigurator.get_initialized_configurations(self.__folder),
        )

    def test_get_serialize_data(self) -> None:
        """Test"""

        self.assertEqual(
            {"language": "Python"}, self.__configurator.get_serialize_data()
        )

    def test_build_gitignore(self) -> None:
        """Test"""

        self.__configurator._build_gitignore()
        with open(
            os.path.join(self.__folder, ".gitignore"), "r", encoding="utf-8"
        ) as file:
            contents = [
                ".DS_Store",
                "env/",
                ".env",
                ".vscode",
                ".venv/",
                "__pycache__/",
                "*.py[cod]",
                "*.log",
            ]
            for expect, actual in zip(contents, file):
                self.assertEqual(expect, actual.split("\n")[0])

    def test_build_configurations(self) -> None:
        """Test"""

        self.__configurator.build_configurations()
        self.assertFalse(
            os.path.isfile(os.path.join(self.__folder, ".gitignore"))
        )

        self.__attributes[".gitignore"] = None
        self.__configurator = PythonConfigurator(self.__attributes)
        self.__configurator.build_configurations()
        self.assertTrue(
            os.path.isfile(os.path.join(self.__folder, ".gitignore"))
        )


if __name__ == "__main__":
    unittest.main()
