# cambai.DubApi

All URIs are relative to *https://client.camb.ai/apis*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_dubbed_output_in_alt_format_status_by_id**](DubApi.md#get_dubbed_output_in_alt_format_status_by_id) | **GET** /dub-alt-format/{task_id} | Get Dubbed Output in Alt Format Status
[**get_dubbed_run_transcript**](DubApi.md#get_dubbed_run_transcript) | **GET** /transcript/{run_id}/{language} | Get Dubbed Run Transcript
[**request_dubbed_output_in_alt_format**](DubApi.md#request_dubbed_output_in_alt_format) | **POST** /dub-alt-format/{run_id}/{language} | Get Dubbed Output in Alt Format


# **get_dubbed_output_in_alt_format_status_by_id**
> TaskStatus get_dubbed_output_in_alt_format_status_by_id(task_id)

Get Dubbed Output in Alt Format Status

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
    api_instance = cambai.DubApi(api_client)
    task_id = 'task_id_example' # str | 

    try:
        # Get Dubbed Output in Alt Format Status
        api_response = api_instance.get_dubbed_output_in_alt_format_status_by_id(task_id)
        print("The response of DubApi->get_dubbed_output_in_alt_format_status_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DubApi->get_dubbed_output_in_alt_format_status_by_id: %s\n" % e)
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

# **get_dubbed_run_transcript**
> get_dubbed_run_transcript(run_id, language, format_type=format_type, data_type=data_type)

Get Dubbed Run Transcript

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
from cambai.models.languages import Languages
from cambai.models.transcript_data_type import TranscriptDataType
from cambai.models.transcript_file_format import TranscriptFileFormat
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
    api_instance = cambai.DubApi(api_client)
    run_id = 56 # int | 
    language = cambai.Languages() # Languages | 
    format_type = txt # TranscriptFileFormat | The format to use for the transcription output. Either `srt`, `vtt` or `txt`. Defaults to `txt`. (optional) (default to txt)
    data_type = file # TranscriptDataType | The data type for the transcription being returned. Returns the raw data of the transcription or a presigned url for the file that contains the transcript contents in the specified format. (optional) (default to file)

    try:
        # Get Dubbed Run Transcript
        api_instance.get_dubbed_run_transcript(run_id, language, format_type=format_type, data_type=data_type)
    except Exception as e:
        print("Exception when calling DubApi->get_dubbed_run_transcript: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **run_id** | **int**|  | 
 **language** | [**Languages**](.md)|  | 
 **format_type** | [**TranscriptFileFormat**](.md)| The format to use for the transcription output. Either &#x60;srt&#x60;, &#x60;vtt&#x60; or &#x60;txt&#x60;. Defaults to &#x60;txt&#x60;. | [optional] [default to txt]
 **data_type** | [**TranscriptDataType**](.md)| The data type for the transcription being returned. Returns the raw data of the transcription or a presigned url for the file that contains the transcript contents in the specified format. | [optional] [default to file]

### Return type

void (empty response body)

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **request_dubbed_output_in_alt_format**
> RequestDubbedOutputInAltFormat200Response request_dubbed_output_in_alt_format(run_id, language, dubbed_output_in_alt_format_request_payload)

Get Dubbed Output in Alt Format

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
from cambai.models.dubbed_output_in_alt_format_request_payload import DubbedOutputInAltFormatRequestPayload
from cambai.models.languages import Languages
from cambai.models.request_dubbed_output_in_alt_format200_response import RequestDubbedOutputInAltFormat200Response
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
    api_instance = cambai.DubApi(api_client)
    run_id = 56 # int | 
    language = cambai.Languages() # Languages | 
    dubbed_output_in_alt_format_request_payload = cambai.DubbedOutputInAltFormatRequestPayload() # DubbedOutputInAltFormatRequestPayload | 

    try:
        # Get Dubbed Output in Alt Format
        api_response = api_instance.request_dubbed_output_in_alt_format(run_id, language, dubbed_output_in_alt_format_request_payload)
        print("The response of DubApi->request_dubbed_output_in_alt_format:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DubApi->request_dubbed_output_in_alt_format: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **run_id** | **int**|  | 
 **language** | [**Languages**](.md)|  | 
 **dubbed_output_in_alt_format_request_payload** | [**DubbedOutputInAltFormatRequestPayload**](DubbedOutputInAltFormatRequestPayload.md)|  | 

### Return type

[**RequestDubbedOutputInAltFormat200Response**](RequestDubbedOutputInAltFormat200Response.md)

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

