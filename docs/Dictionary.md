# Dictionary


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | The unique identifier of the dictionary. | [optional] 
**name** | **str** | The name of the dictionary. | [optional] 
**description** | **str** | A brief description of the dictionary. | [optional] 
**created_at** | **datetime** | The date and time when the dictionary was created. | [optional] 
**updated_at** | **datetime** | The date and time when the dictionary was last updated. | [optional] 

## Example

```python
from cambai.models.dictionary import Dictionary

# TODO update the JSON string below
json = "{}"
# create an instance of Dictionary from a JSON string
dictionary_instance = Dictionary.from_json(json)
# print the JSON string representation of the object
print(Dictionary.to_json())

# convert the object into a dict
dictionary_dict = dictionary_instance.to_dict()
# create an instance of Dictionary from a dict
dictionary_from_dict = Dictionary.from_dict(dictionary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


