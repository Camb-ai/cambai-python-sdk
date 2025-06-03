# CreateTextToVoiceRequestPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**text** | **str** | The text content that will be converted into synthesized speech. | 
**voice_description** | **str** | A detailed description of the desired voice characteristics to guide the synthesis engine. You can specify attributes such as gender, age, accent, emotional tone, speaking style, or cultural context to create authentic voices. | 

## Example

```python
from cambai.models.create_text_to_voice_request_payload import CreateTextToVoiceRequestPayload

# TODO update the JSON string below
json = "{}"
# create an instance of CreateTextToVoiceRequestPayload from a JSON string
create_text_to_voice_request_payload_instance = CreateTextToVoiceRequestPayload.from_json(json)
# print the JSON string representation of the object
print(CreateTextToVoiceRequestPayload.to_json())

# convert the object into a dict
create_text_to_voice_request_payload_dict = create_text_to_voice_request_payload_instance.to_dict()
# create an instance of CreateTextToVoiceRequestPayload from a dict
create_text_to_voice_request_payload_from_dict = CreateTextToVoiceRequestPayload.from_dict(create_text_to_voice_request_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


