"""
Test /app/services/project_serialization.py
"""

import os
import shutil
import unittest

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
            tuple("Python"), ProjectSerializor.get_supported_langauges()
        )

    def test_serialize_deserialize(self) -> None:
        """Test serialize and deserialize"""

        # Success
        ProjectSerializor.create_configuration_folder(self.__folder)
        attributes = {"language": "Python", "Framework": "Flask"}
        ProjectSerializor.serialize(self.__folder, attributes)
        deserialized = ProjectSerializor.deserialize(self.__folder)
        self.assertEqual(attributes, deserialized)

        # Fail
        with self.assertRaises(NotADirectoryError):
            ProjectSerializor.serialize(self.__folder + "a", attributes)
        with self.assertRaises(FileNotFoundError):
            ProjectSerializor.deserialize(self.__folder + "a")


if __name__ == "__main__":
    unittest.main()
