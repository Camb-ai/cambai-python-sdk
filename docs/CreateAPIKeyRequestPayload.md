# CreateAPIKeyRequestPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**team_id** | **int** |  | 

## Example

```python
from cambai.models.create_api_key_request_payload import CreateAPIKeyRequestPayload

# TODO update the JSON string below
json = "{}"
# create an instance of CreateAPIKeyRequestPayload from a JSON string
create_api_key_request_payload_instance = CreateAPIKeyRequestPayload.from_json(json)
# print the JSON string representation of the object
print(CreateAPIKeyRequestPayload.to_json())

# convert the object into a dict
create_api_key_request_payload_dict = create_api_key_request_payload_instance.to_dict()
# create an instance of CreateAPIKeyRequestPayload from a dict
create_api_key_request_payload_from_dict = CreateAPIKeyRequestPayload.from_dict(create_api_key_request_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


