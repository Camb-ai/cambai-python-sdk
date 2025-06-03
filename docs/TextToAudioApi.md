# cambai.TextToAudioApi

All URIs are relative to *https://client.camb.ai/apis*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_text_to_sound**](TextToAudioApi.md#create_text_to_sound) | **POST** /text-to-sound | Create Text to Sound
[**get_text_to_audio_status_by_id**](TextToAudioApi.md#get_text_to_audio_status_by_id) | **GET** /text-to-sound/{task_id} | Get Text To Audio Status
[**get_text_to_sound_run_result_by_id**](TextToAudioApi.md#get_text_to_sound_run_result_by_id) | **GET** /text-to-sound-result/{run_id} | Get Text to Sound Run Result


# **create_text_to_sound**
> TaskID create_text_to_sound(create_text_to_audio_request_payload)

Create Text to Sound

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
from cambai.models.create_text_to_audio_request_payload import CreateTextToAudioRequestPayload
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
    api_instance = cambai.TextToAudioApi(api_client)
    create_text_to_audio_request_payload = cambai.CreateTextToAudioRequestPayload() # CreateTextToAudioRequestPayload | 

    try:
        # Create Text to Sound
        api_response = api_instance.create_text_to_sound(create_text_to_audio_request_payload)
        print("The response of TextToAudioApi->create_text_to_sound:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TextToAudioApi->create_text_to_sound: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_text_to_audio_request_payload** | [**CreateTextToAudioRequestPayload**](CreateTextToAudioRequestPayload.md)|  | 

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

# **get_text_to_audio_status_by_id**
> OrchestratorPipelineResult get_text_to_audio_status_by_id(task_id)

Get Text To Audio Status

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
    api_instance = cambai.TextToAudioApi(api_client)
    task_id = 'task_id_example' # str | 

    try:
        # Get Text To Audio Status
        api_response = api_instance.get_text_to_audio_status_by_id(task_id)
        print("The response of TextToAudioApi->get_text_to_audio_status_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TextToAudioApi->get_text_to_audio_status_by_id: %s\n" % e)
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
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_text_to_sound_run_result_by_id**
> bytearray get_text_to_sound_run_result_by_id(run_id)

Get Text to Sound Run Result

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
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
    api_instance = cambai.TextToAudioApi(api_client)
    run_id = 56 # int | The unique identifier for the run, which was generated during the text to an audio effect creation process and returned upon task completion.

    try:
        # Get Text to Sound Run Result
        api_response = api_instance.get_text_to_sound_run_result_by_id(run_id)
        print("The response of TextToAudioApi->get_text_to_sound_run_result_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TextToAudioApi->get_text_to_sound_run_result_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **run_id** | **int**| The unique identifier for the run, which was generated during the text to an audio effect creation process and returned upon task completion. | 

### Return type

**bytearray**

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: audio/wav, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

