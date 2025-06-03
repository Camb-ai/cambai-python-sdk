# CreateTranslatedStoryRequestPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**target_language** | [**Languages**](Languages.md) | The lang | [optional] 

## Example

```python
from cambai.models.create_translated_story_request_payload import CreateTranslatedStoryRequestPayload

# TODO update the JSON string below
json = "{}"
# create an instance of CreateTranslatedStoryRequestPayload from a JSON string
create_translated_story_request_payload_instance = CreateTranslatedStoryRequestPayload.from_json(json)
# print the JSON string representation of the object
print(CreateTranslatedStoryRequestPayload.to_json())

# convert the object into a dict
create_translated_story_request_payload_dict = create_translated_story_request_payload_instance.to_dict()
# create an instance of CreateTranslatedStoryRequestPayload from a dict
create_translated_story_request_payload_from_dict = CreateTranslatedStoryRequestPayload.from_dict(create_translated_story_request_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


