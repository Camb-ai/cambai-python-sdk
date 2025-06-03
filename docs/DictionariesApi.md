# cambai.DictionariesApi

All URIs are relative to *https://client.camb.ai/apis*

Method | HTTP request | Description
------------- | ------------- | -------------
[**dictionaries_get**](DictionariesApi.md#dictionaries_get) | **GET** /dictionaries | Get Workspace Dictionaries


# **dictionaries_get**
> List[Dictionary] dictionaries_get()

Get Workspace Dictionaries

Get a list of dictionaries in the workspace.

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
from cambai.models.dictionary import Dictionary
from cambai.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://client.camb.ai/apis
# See configuration.py for a list of all supported configuration parameters.
configuration = cambai.Configuration(
    host = "https://client.camb.ai/apis"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: APIKeyHeader
configuration.api_key['APIKeyHeader'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['APIKeyHeader'] = 'Bearer'

# Enter a context with an instance of the API client
with cambai.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = cambai.DictionariesApi(api_client)

    try:
        # Get Workspace Dictionaries
        api_response = api_instance.dictionaries_get()
        print("The response of DictionariesApi->dictionaries_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DictionariesApi->dictionaries_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[Dictionary]**](Dictionary.md)

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

