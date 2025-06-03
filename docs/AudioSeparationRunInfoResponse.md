# AudioSeparationRunInfoResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**foreground_audio_url** | **str** | The URL pointing to the generated audio file for the detected foreground audio. | [optional] 
**background_audio_url** | **str** | The URL pointing to the generated audio file for the detected background audio. | [optional] 

## Example

```python
from cambai.models.audio_separation_run_info_response import AudioSeparationRunInfoResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AudioSeparationRunInfoResponse from a JSON string
audio_separation_run_info_response_instance = AudioSeparationRunInfoResponse.from_json(json)
# print the JSON string representation of the object
print(AudioSeparationRunInfoResponse.to_json())

# convert the object into a dict
audio_separation_run_info_response_dict = audio_separation_run_info_response_instance.to_dict()
# create an instance of AudioSeparationRunInfoResponse from a dict
audio_separation_run_info_response_from_dict = AudioSeparationRunInfoResponse.from_dict(audio_separation_run_info_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


