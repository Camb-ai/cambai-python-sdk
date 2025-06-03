# DialogueItem

A JSON that represents a single piece of dialogue or speech within a given time range. It includes details about the timing (start and end), the content of the dialogue (text), and the speaker who delivers the dialogue

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start** | **float** | The start time (in seconds) of the dialogue. | 
**end** | **float** | The end time (in seconds) of the dialogue. | 
**text** | **str** | The actual text content of the dialogue spoken by the speaker. | 
**speaker** | **str** | The name or identifier of the speaker delivering the dialogue. | 

## Example

```python
from cambai.models.dialogue_item import DialogueItem

# TODO update the JSON string below
json = "{}"
# create an instance of DialogueItem from a JSON string
dialogue_item_instance = DialogueItem.from_json(json)
# print the JSON string representation of the object
print(DialogueItem.to_json())

# convert the object into a dict
dialogue_item_dict = dialogue_item_instance.to_dict()
# create an instance of DialogueItem from a dict
dialogue_item_from_dict = DialogueItem.from_dict(dialogue_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


