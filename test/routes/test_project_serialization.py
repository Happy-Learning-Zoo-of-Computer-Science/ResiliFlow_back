"""Test select project APIs.
"""

import os
import shutil
import unittest

from app import create_app


class MyTestCase(unittest.TestCase):
    """A test case."""

    def setUp(self) -> None:
        app = create_app()
        app.config["TESTING"] = True
        self.client = app.test_client()
        self.__folder = "test_folder"
        os.mkdir(self.__folder)

    def tearDown(self) -> None:
        shutil.rmtree(self.__folder)

    def test_get_supported_languages(self) -> None:
        """Test GET /api/project/languages"""

        response = self.client.get("/api/project/languages")
        self.assertEqual(200, response.status_code)
        self.assertEqual(["Python"], response.get_json())

    def test_get_support_frameworks(self) -> None:
        """Test GET /api/project/frameworks"""
        
        api = "/api/project/frameworks"
        payload = {"language": "Python"}
        response = self.client.get(api, json=payload)
        self.assertEqual(0, len(response.get_json()))

        payload["language"] = "JavaScript"
        response = self.client.get(api, json=payload)
        self.assertEqual(0, len(response.get_json()))

        payload.pop("language")
        response = self.client.get(api, json=payload)
        self.assertEqual(400, response.status_code)

        response = self.client.get(api)
        self.assertEqual(415, response.status_code)

    def test_get_supported_configurations(self) -> None:
        """Test GET /api/project/configurations/supported"""

        api = "/api/project/configurations/supported"
        
        payload = {"language": "Python"}
        response = self.client.get(api, json=payload)
        self.assertEqual(1, len(response.get_json()))
        self.assertEqual({".gitignore": None}, response.get_json())

        payload["language"] = "JavaScript"
        response = self.client.get(api, json=payload)
        self.assertEqual(0, len(response.get_json()))

        payload.pop("language")
        response = self.client.get(api, json=payload)
        self.assertEqual(400, response.status_code)

        response = self.client.get(api)
        self.assertEqual(415, response.status_code)

    def test_get_initialized_configuration(self) -> None:
        """Test GET /api/project/configurations/initialized"""

        api = "/api/project/configurations/initialized"
        
        payload = {"language": "Python", "path": self.__folder}
        response = self.client.get(api, json=payload)
        self.assertEqual(0, len(response.get_json()))

        payload[".gitignore"] = None
        self.client.post("/api/project/create", json=payload)
        response = self.client.get(api, json=payload)
        self.assertEqual(1, len(response.get_json()))
        self.assertIn(".gitignore", response.get_json())

        payload["path"] = payload["path"] + "a"
        response = self.client.get(api, json=payload)
        self.assertEqual(400, response.status_code)
        self.assertEqual(f'Path "{payload["path"]}" does not exist.', response.get_json()["error"])

        payload.pop("path")
        response = self.client.get(api, json=payload)
        self.assertEqual(400, response.status_code)
        self.assertEqual('Missing field "path".', response.get_json()["error"])

        payload.pop("language")
        response = self.client.get(api, json=payload)
        self.assertEqual(400, response.status_code)
        self.assertEqual('Missing field "language".', response.get_json()["error"])

    def test_is_project_initialized(self) -> None:
        """Test GET /api/project/validate"""

        api = "/api/project/validate"
        # Success
        payload = {"path": os.path.join(os.curdir, self.__folder)}
        response = self.client.get(api, json=payload)
        self.assertEqual(200, response.status_code)
        self.assertFalse(response.get_json()["valid"])

        payload["language"] = "Python"
        self.client.post("/api/project/create", json=payload)
        response = self.client.get(api, json=payload)
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.get_json()["valid"])

        # Fail
        payload.pop("path")
        response = self.client.get(api, json=payload)
        self.assertEqual(400, response.status_code)

    def test_create_project(self) -> None:
        """Test /api/project/create"""

        api = "/api/project/create"

        # Success
        payload = {
            "path": os.path.join(os.curdir, self.__folder),
            "language": "Python",
        }
        response = self.client.post(api, json=payload)
        self.assertEqual(200, response.status_code)
        self.assertTrue(
            os.path.isfile(
                os.path.join(self.__folder, ".hlzcs/project_attributes.yaml")
            )
        )

        # Fail
        payload["language"] = "JavaScript"
        response = self.client.post(api, json=payload)
        self.assertEqual(400, response.status_code)

        payload.pop("language")
        response = self.client.post(api, json=payload)
        self.assertEqual(400, response.status_code)

        payload["language"] = "Python"
        payload["path"] = payload["path"] + "a"
        response = self.client.post(api, json=payload)
        self.assertEqual(400, response.status_code)

        payload.pop("path")
        response = self.client.post(api, json=payload)
        self.assertEqual(400, response.status_code)


if __name__ == "__main__":
    unittest.main()
