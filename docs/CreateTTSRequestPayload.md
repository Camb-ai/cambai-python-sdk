# CreateTTSRequestPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**text** | **str** | The text to be converted to speech | 
**voice_id** | **int** | The voice ID to be used to generate speech. | 
**language** | [**Languages**](Languages.md) | The language in which the provided text is written in. | 
**gender** | [**Gender**](Gender.md) |  | [optional] 
**age** | **object** |  | [optional] 

## Example

```python
from cambai.models.create_tts_request_payload import CreateTTSRequestPayload

# TODO update the JSON string below
json = "{}"
# create an instance of CreateTTSRequestPayload from a JSON string
create_tts_request_payload_instance = CreateTTSRequestPayload.from_json(json)
# print the JSON string representation of the object
print(CreateTTSRequestPayload.to_json())

# convert the object into a dict
create_tts_request_payload_dict = create_tts_request_payload_instance.to_dict()
# create an instance of CreateTTSRequestPayload from a dict
create_tts_request_payload_from_dict = CreateTTSRequestPayload.from_dict(create_tts_request_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


