# CreateTranslationStreamRequestPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**text** | **str** |  | 
**source_language** | [**Languages**](Languages.md) |  | 
**target_language** | [**Languages**](Languages.md) |  | 
**formality** | [**Formalities**](Formalities.md) |  | [optional] 
**gender** | [**Gender**](Gender.md) |  | [optional] 

## Example

```python
from cambai.models.create_translation_stream_request_payload import CreateTranslationStreamRequestPayload

# TODO update the JSON string below
json = "{}"
# create an instance of CreateTranslationStreamRequestPayload from a JSON string
create_translation_stream_request_payload_instance = CreateTranslationStreamRequestPayload.from_json(json)
# print the JSON string representation of the object
print(CreateTranslationStreamRequestPayload.to_json())

# convert the object into a dict
create_translation_stream_request_payload_dict = create_translation_stream_request_payload_instance.to_dict()
# create an instance of CreateTranslationStreamRequestPayload from a dict
create_translation_stream_request_payload_from_dict = CreateTranslationStreamRequestPayload.from_dict(create_translation_stream_request_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


