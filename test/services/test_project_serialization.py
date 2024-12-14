"""
Test /app/services/project_serialization.py
"""

import os
import shutil
import unittest

import yaml

from app.services.project_serialization import ProjectSerializor


class MyTestCase(unittest.TestCase):
    """Test case.

    Args:
        unittest (_type_): Unit test.
    """

    def setUp(self) -> None:
        # Create a folder.
        self.__folder = "test_folder"
        os.mkdir(self.__folder)
        self.__folder = os.path.join(os.path.curdir, self.__folder)

    def tearDown(self) -> None:
        # Delete the folder.
        shutil.rmtree(self.__folder)

    def test_create_configuration(self) -> None:
        """Test create_configuration_folder and is_initialized"""

        # Success
        self.assertFalse(ProjectSerializor.is_initialized(self.__folder))
        ProjectSerializor.create_configuration_folder(self.__folder)
        self.assertTrue(ProjectSerializor.is_initialized(self.__folder))

        # Fail
        with self.assertRaises(NotADirectoryError):
            ProjectSerializor.create_configuration_folder(self.__folder + "a")

    def test_get_supported_languages(self) -> None:
        """Test get_supported_languages"""
        self.assertEqual(
            tuple(["Python"]), ProjectSerializor.get_supported_langauges()
        )

    def test_serialize_deserialize(self) -> None:
        """Test serialize and deserialize"""

        # Success
        ProjectSerializor.create_configuration_folder(self.__folder)
        attributes = {"path": self.__folder, "language": "Python"}
        ProjectSerializor.serialize(self.__folder, attributes)
        deserialized = ProjectSerializor.deserialize(self.__folder)
        self.assertEqual(attributes, deserialized)

        # Fail
        with self.assertRaises(NotADirectoryError):
            ProjectSerializor.serialize(self.__folder + "a", attributes)

        with self.assertRaises(FileNotFoundError):
            ProjectSerializor.deserialize(self.__folder + "a")

        with open(
            os.path.join(self.__folder, ".hlzcs/project_attributes.yaml"),
            "w",
            encoding="utf-8",
        ) as file:
            yaml.dump({"framework": "Flask"}, file)

        with self.assertRaises(KeyError):
            ProjectSerializor.deserialize(self.__folder)

        with open(
            os.path.join(self.__folder, ".hlzcs/project_attributes.yaml"),
            "w",
            encoding="utf-8",
        ) as file:
            yaml.dump({"language": "JavaScript"}, file)
        with self.assertRaises(ValueError):
            ProjectSerializor.deserialize(self.__folder)

    def test_create_project(self) -> None:
        """Test create_project."""

        # Success
        data = {"path": self.__folder, "language": "Python"}
        ProjectSerializor.create_project(data)
        self.assertEqual(
            "Python", ProjectSerializor.deserialize(self.__folder)["language"]
        )

        # Fail

        data["path"] = self.__folder + "A"
        with self.assertRaises(NotADirectoryError):
            ProjectSerializor.create_project(data)

        data.pop("path")
        with self.assertRaises(KeyError):
            ProjectSerializor.create_project(data)

        data["path"] = self.__folder
        data["language"] = "JavaScript"
        with self.assertRaises(ValueError):
            ProjectSerializor.create_project(data)

        data.pop("language")
        with self.assertRaises(KeyError):
            ProjectSerializor.create_project(data)


if __name__ == "__main__":
    unittest.main()
