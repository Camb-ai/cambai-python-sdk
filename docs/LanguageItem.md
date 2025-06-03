# LanguageItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | The id property represents a unique numerical identifier assigned to each language in the system. | [optional] 
**language** | **str** | The language property represents the full, human-readable name of a language and its associated regional or country variant. | [optional] 
**short_name** | **str** | The short name is a standardized identifier for each language and locale combination, represented in the format of &lt;language code&gt;-&lt;country code&gt;. | [optional] 

## Example

```python
from cambai.models.language_item import LanguageItem

# TODO update the JSON string below
json = "{}"
# create an instance of LanguageItem from a JSON string
language_item_instance = LanguageItem.from_json(json)
# print the JSON string representation of the object
print(LanguageItem.to_json())

# convert the object into a dict
language_item_dict = language_item_instance.to_dict()
# create an instance of LanguageItem from a dict
language_item_from_dict = LanguageItem.from_dict(language_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


