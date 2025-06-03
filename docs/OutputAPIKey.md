# OutputAPIKey


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**api_key** | **str** |  | 
**api_key_name** | **str** |  | [optional] 
**created_at** | **datetime** |  | 
**expiry_time** | **datetime** |  | 
**team_id** | **int** |  | 
**is_valid** | **bool** |  | 

## Example

```python
from cambai.models.output_api_key import OutputAPIKey

# TODO update the JSON string below
json = "{}"
# create an instance of OutputAPIKey from a JSON string
output_api_key_instance = OutputAPIKey.from_json(json)
# print the JSON string representation of the object
print(OutputAPIKey.to_json())

# convert the object into a dict
output_api_key_dict = output_api_key_instance.to_dict()
# create an instance of OutputAPIKey from a dict
output_api_key_from_dict = OutputAPIKey.from_dict(output_api_key_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


