# AudioOutputFileURLResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**output_url** | **str** | A presigned URL that points to the output audio file. | [optional] 

## Example

```python
from cambai.models.audio_output_file_url_response import AudioOutputFileURLResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AudioOutputFileURLResponse from a JSON string
audio_output_file_url_response_instance = AudioOutputFileURLResponse.from_json(json)
# print the JSON string representation of the object
print(AudioOutputFileURLResponse.to_json())

# convert the object into a dict
audio_output_file_url_response_dict = audio_output_file_url_response_instance.to_dict()
# create an instance of AudioOutputFileURLResponse from a dict
audio_output_file_url_response_from_dict = AudioOutputFileURLResponse.from_dict(audio_output_file_url_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


