# CreateTextToAudioRequestPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prompt** | **str** | The text to be converted to audio. | [optional] 
**duration** | **float** | The desired duration of the audio. | [optional] [default to 8.0]

## Example

```python
from cambai.models.create_text_to_audio_request_payload import CreateTextToAudioRequestPayload

# TODO update the JSON string below
json = "{}"
# create an instance of CreateTextToAudioRequestPayload from a JSON string
create_text_to_audio_request_payload_instance = CreateTextToAudioRequestPayload.from_json(json)
# print the JSON string representation of the object
print(CreateTextToAudioRequestPayload.to_json())

# convert the object into a dict
create_text_to_audio_request_payload_dict = create_text_to_audio_request_payload_instance.to_dict()
# create an instance of CreateTextToAudioRequestPayload from a dict
create_text_to_audio_request_payload_from_dict = CreateTextToAudioRequestPayload.from_dict(create_text_to_audio_request_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


