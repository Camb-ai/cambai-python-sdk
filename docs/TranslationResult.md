# TranslationResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**texts** | **List[str]** | An array of strings containing the translated output texts. Each item in the array corresponds to one translated text | [optional] 

## Example

```python
from cambai.models.translation_result import TranslationResult

# TODO update the JSON string below
json = "{}"
# create an instance of TranslationResult from a JSON string
translation_result_instance = TranslationResult.from_json(json)
# print the JSON string representation of the object
print(TranslationResult.to_json())

# convert the object into a dict
translation_result_dict = translation_result_instance.to_dict()
# create an instance of TranslationResult from a dict
translation_result_from_dict = TranslationResult.from_dict(translation_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


