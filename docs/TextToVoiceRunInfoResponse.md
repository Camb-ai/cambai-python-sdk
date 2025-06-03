# TextToVoiceRunInfoResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**previews** | **List[str]** | An array of three distinct URL strings, each pointing to a unique voice sample generated from your text prompt. These samples represent different voice interpretations based on your description, allowing you to compare options before selecting your preferred voice for further use.  | [optional] 

## Example

```python
from cambai.models.text_to_voice_run_info_response import TextToVoiceRunInfoResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TextToVoiceRunInfoResponse from a JSON string
text_to_voice_run_info_response_instance = TextToVoiceRunInfoResponse.from_json(json)
# print the JSON string representation of the object
print(TextToVoiceRunInfoResponse.to_json())

# convert the object into a dict
text_to_voice_run_info_response_dict = text_to_voice_run_info_response_instance.to_dict()
# create an instance of TextToVoiceRunInfoResponse from a dict
text_to_voice_run_info_response_from_dict = TextToVoiceRunInfoResponse.from_dict(text_to_voice_run_info_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


