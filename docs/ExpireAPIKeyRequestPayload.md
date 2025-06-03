# ExpireAPIKeyRequestPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**api_key_id** | **int** |  | 

## Example

```python
from cambai.models.expire_api_key_request_payload import ExpireAPIKeyRequestPayload

# TODO update the JSON string below
json = "{}"
# create an instance of ExpireAPIKeyRequestPayload from a JSON string
expire_api_key_request_payload_instance = ExpireAPIKeyRequestPayload.from_json(json)
# print the JSON string representation of the object
print(ExpireAPIKeyRequestPayload.to_json())

# convert the object into a dict
expire_api_key_request_payload_dict = expire_api_key_request_payload_instance.to_dict()
# create an instance of ExpireAPIKeyRequestPayload from a dict
expire_api_key_request_payload_from_dict = ExpireAPIKeyRequestPayload.from_dict(expire_api_key_request_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


