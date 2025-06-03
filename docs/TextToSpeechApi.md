# cambai.TextToSpeechApi

All URIs are relative to *https://client.camb.ai/apis*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_tts**](TextToSpeechApi.md#create_tts) | **POST** /tts | Create Tts
[**get_tts_result_by_id**](TextToSpeechApi.md#get_tts_result_by_id) | **GET** /tts/{id} | Get Tts Result


# **create_tts**
> TaskID create_tts(create_tts_request_payload)

Create Tts

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
from cambai.models.create_tts_request_payload import CreateTTSRequestPayload
from cambai.models.task_id import TaskID
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
    api_instance = cambai.TextToSpeechApi(api_client)
    create_tts_request_payload = cambai.CreateTTSRequestPayload() # CreateTTSRequestPayload | 

    try:
        # Create Tts
        api_response = api_instance.create_tts(create_tts_request_payload)
        print("The response of TextToSpeechApi->create_tts:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TextToSpeechApi->create_tts: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_tts_request_payload** | [**CreateTTSRequestPayload**](CreateTTSRequestPayload.md)|  | 

### Return type

[**TaskID**](TaskID.md)

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_tts_result_by_id**
> OrchestratorPipelineResult get_tts_result_by_id(id)

Get Tts Result

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
from cambai.models.orchestrator_pipeline_result import OrchestratorPipelineResult
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
    api_instance = cambai.TextToSpeechApi(api_client)
    id = 'id_example' # str | 

    try:
        # Get Tts Result
        api_response = api_instance.get_tts_result_by_id(id)
        print("The response of TextToSpeechApi->get_tts_result_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TextToSpeechApi->get_tts_result_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**OrchestratorPipelineResult**](OrchestratorPipelineResult.md)

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

