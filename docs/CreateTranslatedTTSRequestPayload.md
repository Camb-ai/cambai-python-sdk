# CreateTranslatedTTSRequestPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**text** | **str** |  | 
**voice_id** | **int** |  | 
**age** | **int** |  | [optional] 
**formality** | [**Formalities**](Formalities.md) |  | [optional] 
**gender** | [**Gender**](Gender.md) |  | [optional] 
**source_language** | [**Languages**](Languages.md) |  | 
**target_language** | [**Languages**](Languages.md) |  | 
**chosen_dictionaries** | **List[int]** | An optional list of dictionary IDs selected by the user. Each entry must be an integer corresponding to a valid dictionary ID. If provided, at least one ID is required. | [optional] 

## Example

```python
from cambai.models.create_translated_tts_request_payload import CreateTranslatedTTSRequestPayload

# TODO update the JSON string below
json = "{}"
# create an instance of CreateTranslatedTTSRequestPayload from a JSON string
create_translated_tts_request_payload_instance = CreateTranslatedTTSRequestPayload.from_json(json)
# print the JSON string representation of the object
print(CreateTranslatedTTSRequestPayload.to_json())

# convert the object into a dict
create_translated_tts_request_payload_dict = create_translated_tts_request_payload_instance.to_dict()
# create an instance of CreateTranslatedTTSRequestPayload from a dict
create_translated_tts_request_payload_from_dict = CreateTranslatedTTSRequestPayload.from_dict(create_translated_tts_request_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


