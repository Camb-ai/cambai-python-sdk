# VoiceItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | A unique identifier for the voice record. Each voice is assigned a distinct &#x60;id&#x60; for reference | [optional] 
**voice_name** | **str** | The name or label assigned to the voice. | [optional] 
**gender** | **int** | Represents the gender of the voice. Values are encoded as integers. | [optional] 
**age** | **int** | The age of the voice represented as an integer. If the age is unknown or not applicable, the value is &#x60;null&#x60;. | [optional] 
**description** | **str** | A brief summary of the custom voice—e.g. its intended use, tone or character traits. | [optional] 
**transcript** | **str** | The transcribed text of the voice recording, if available. | [optional] 
**is_published** | **bool** | Specifies whether the voice is shared on the marketplace or not. | [optional] 
**language** | [**Languages**](Languages.md) | The language specified when creating the custom voice. | [optional] 

## Example

```python
from cambai.models.voice_item import VoiceItem

# TODO update the JSON string below
json = "{}"
# create an instance of VoiceItem from a JSON string
voice_item_instance = VoiceItem.from_json(json)
# print the JSON string representation of the object
print(VoiceItem.to_json())

# convert the object into a dict
voice_item_dict = voice_item_instance.to_dict()
# create an instance of VoiceItem from a dict
voice_item_from_dict = VoiceItem.from_dict(voice_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


