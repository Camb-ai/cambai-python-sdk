# coding: utf-8

"""
    FastAPI

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from cambai.models.end_to_end_dubbing_request_payload import EndToEndDubbingRequestPayload

class TestEndToEndDubbingRequestPayload(unittest.TestCase):
    """EndToEndDubbingRequestPayload unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> EndToEndDubbingRequestPayload:
        """Test EndToEndDubbingRequestPayload
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `EndToEndDubbingRequestPayload`
        """
        model = EndToEndDubbingRequestPayload()
        if include_optional:
            return EndToEndDubbingRequestPayload(
                video_url = '',
                source_language = 1,
                target_languages = [
                    1
                    ],
                selected_audio_tracks = [
                    56
                    ],
                add_output_as_an_audio_track = True,
                chosen_dictionaries = [
                    56
                    ]
            )
        else:
            return EndToEndDubbingRequestPayload(
                video_url = '',
                source_language = 1,
        )
        """

    def testEndToEndDubbingRequestPayload(self):
        """Test EndToEndDubbingRequestPayload"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
