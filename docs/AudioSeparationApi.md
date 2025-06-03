# cambai.AudioSeparationApi

All URIs are relative to *https://client.camb.ai/apis*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_audio_separation**](AudioSeparationApi.md#create_audio_separation) | **POST** /audio-separation | Create Audio Separation
[**get_audio_separation_run_info_by_id**](AudioSeparationApi.md#get_audio_separation_run_info_by_id) | **GET** /audio-separation-result/{run_id} | Get Audio Separation Run Info
[**get_audio_separation_status_by_id**](AudioSeparationApi.md#get_audio_separation_status_by_id) | **GET** /audio-separation/{task_id} | Get Audio Separation Status


# **create_audio_separation**
> TaskID create_audio_separation(audio_file=audio_file)

Create Audio Separation

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
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
    api_instance = cambai.AudioSeparationApi(api_client)
    audio_file = None # bytearray | Media file to processed. AAC, FLAC, MP3 and WAV formats are supported. (optional)

    try:
        # Create Audio Separation
        api_response = api_instance.create_audio_separation(audio_file=audio_file)
        print("The response of AudioSeparationApi->create_audio_separation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AudioSeparationApi->create_audio_separation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **audio_file** | **bytearray**| Media file to processed. AAC, FLAC, MP3 and WAV formats are supported. | [optional] 

### Return type

[**TaskID**](TaskID.md)

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_audio_separation_run_info_by_id**
> AudioSeparationRunInfoResponse get_audio_separation_run_info_by_id(run_id)

Get Audio Separation Run Info

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
from cambai.models.audio_separation_run_info_response import AudioSeparationRunInfoResponse
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
    api_instance = cambai.AudioSeparationApi(api_client)
    run_id = 56 # int | 

    try:
        # Get Audio Separation Run Info
        api_response = api_instance.get_audio_separation_run_info_by_id(run_id)
        print("The response of AudioSeparationApi->get_audio_separation_run_info_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AudioSeparationApi->get_audio_separation_run_info_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **run_id** | **int**|  | 

### Return type

[**AudioSeparationRunInfoResponse**](AudioSeparationRunInfoResponse.md)

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

# **get_audio_separation_status_by_id**
> TaskStatus get_audio_separation_status_by_id(task_id)

Get Audio Separation Status

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
from cambai.models.task_status import TaskStatus
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
    api_instance = cambai.AudioSeparationApi(api_client)
    task_id = 'task_id_example' # str | 

    try:
        # Get Audio Separation Status
        api_response = api_instance.get_audio_separation_status_by_id(task_id)
        print("The response of AudioSeparationApi->get_audio_separation_status_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AudioSeparationApi->get_audio_separation_status_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **task_id** | **str**|  | 

### Return type

[**TaskStatus**](TaskStatus.md)

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

