# coding: utf-8

"""
    FastAPI

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from cambai.api.text_to_voice_api import TextToVoiceApi


class TestTextToVoiceApi(unittest.TestCase):
    """TextToVoiceApi unit test stubs"""

    def setUp(self) -> None:
        self.api = TextToVoiceApi()

    def tearDown(self) -> None:
        pass

    def test_create_voice_from_description(self) -> None:
        """Test case for create_voice_from_description

        Create Voice from Description
        """
        pass

    def test_get_text_to_voice_run_result_by_id(self) -> None:
        """Test case for get_text_to_voice_run_result_by_id

        Get Text-to-Voice Run Result
        """
        pass

    def test_text_to_voice_task_id_get(self) -> None:
        """Test case for text_to_voice_task_id_get

        Get Text-to-Voice Task Status
        """
        pass


if __name__ == '__main__':
    unittest.main()
