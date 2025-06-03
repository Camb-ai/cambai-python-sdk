# cambai.TextToVoiceApi

All URIs are relative to *https://client.camb.ai/apis*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_voice_from_description**](TextToVoiceApi.md#create_voice_from_description) | **POST** /text-to-voice | Create Voice from Description
[**get_text_to_voice_run_result_by_id**](TextToVoiceApi.md#get_text_to_voice_run_result_by_id) | **GET** /text-to-voice-result/{run_id} | Get Text-to-Voice Run Result
[**text_to_voice_task_id_get**](TextToVoiceApi.md#text_to_voice_task_id_get) | **GET** /text-to-voice/{task_id} | Get Text-to-Voice Task Status


# **create_voice_from_description**
> TaskID create_voice_from_description(create_text_to_voice_request_payload)

Create Voice from Description

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
from cambai.models.create_text_to_voice_request_payload import CreateTextToVoiceRequestPayload
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
    api_instance = cambai.TextToVoiceApi(api_client)
    create_text_to_voice_request_payload = cambai.CreateTextToVoiceRequestPayload() # CreateTextToVoiceRequestPayload | 

    try:
        # Create Voice from Description
        api_response = api_instance.create_voice_from_description(create_text_to_voice_request_payload)
        print("The response of TextToVoiceApi->create_voice_from_description:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TextToVoiceApi->create_voice_from_description: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_text_to_voice_request_payload** | [**CreateTextToVoiceRequestPayload**](CreateTextToVoiceRequestPayload.md)|  | 

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
**200** | Successful response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_text_to_voice_run_result_by_id**
> TextToVoiceRunInfoResponse get_text_to_voice_run_result_by_id(run_id)

Get Text-to-Voice Run Result

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
from cambai.models.text_to_voice_run_info_response import TextToVoiceRunInfoResponse
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
    api_instance = cambai.TextToVoiceApi(api_client)
    run_id = 56 # int | The unique identifier for the run, which was generated during the text to voice creation process and returned upon task completion.

    try:
        # Get Text-to-Voice Run Result
        api_response = api_instance.get_text_to_voice_run_result_by_id(run_id)
        print("The response of TextToVoiceApi->get_text_to_voice_run_result_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TextToVoiceApi->get_text_to_voice_run_result_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **run_id** | **int**| The unique identifier for the run, which was generated during the text to voice creation process and returned upon task completion. | 

### Return type

[**TextToVoiceRunInfoResponse**](TextToVoiceRunInfoResponse.md)

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

# **text_to_voice_task_id_get**
> OrchestratorPipelineResult text_to_voice_task_id_get(task_id)

Get Text-to-Voice Task Status

Get the status of a text-to-voice task by its ID.

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
    api_instance = cambai.TextToVoiceApi(api_client)
    task_id = 'task_id_example' # str | 

    try:
        # Get Text-to-Voice Task Status
        api_response = api_instance.text_to_voice_task_id_get(task_id)
        print("The response of TextToVoiceApi->text_to_voice_task_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TextToVoiceApi->text_to_voice_task_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **task_id** | **str**|  | 

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
**200** | Successful response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

