# coding: utf-8

"""
    FastAPI

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from cambai.api.text_to_audio_api import TextToAudioApi


class TestTextToAudioApi(unittest.TestCase):
    """TextToAudioApi unit test stubs"""

    def setUp(self) -> None:
        self.api = TextToAudioApi()

    def tearDown(self) -> None:
        pass

    def test_create_text_to_sound(self) -> None:
        """Test case for create_text_to_sound

        Create Text to Sound
        """
        pass

    def test_get_text_to_audio_status_by_id(self) -> None:
        """Test case for get_text_to_audio_status_by_id

        Get Text To Audio Status
        """
        pass

    def test_get_text_to_sound_run_result_by_id(self) -> None:
        """Test case for get_text_to_sound_run_result_by_id

        Get Text to Sound Run Result
        """
        pass


if __name__ == '__main__':
    unittest.main()
