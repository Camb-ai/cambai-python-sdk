# cambai.StoriesApi

All URIs are relative to *https://client.camb.ai/apis*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_story**](StoriesApi.md#create_story) | **POST** /story | Create Story
[**create_translated_story**](StoriesApi.md#create_translated_story) | **POST** /translated-story/{run_id} | Create Translated Story
[**get_story_run_info_by_id**](StoriesApi.md#get_story_run_info_by_id) | **GET** /story-result/{run_id} | Get Story Run Info
[**get_translated_story_run_info**](StoriesApi.md#get_translated_story_run_info) | **GET** /translated-story-result/{run_id}/{target_language} | Get Translated Story Run Info
[**get_translated_story_status_by_id**](StoriesApi.md#get_translated_story_status_by_id) | **GET** /translated-story/{task_id} | Get Translated Story Status


# **create_story**
> TaskID create_story(file, source_language, title=title, description=description, narrator_voice_id=narrator_voice_id, chosen_dictionaries=chosen_dictionaries)

Create Story

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
from cambai.models.languages import Languages
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
    api_instance = cambai.StoriesApi(api_client)
    file = None # bytearray | The text file (`.txt`) or Word document (`.docx`) that its contents will be used for creating a story.
    source_language = cambai.Languages() # Languages | The language of the contents in the input file.
    title = 'title_example' # str | The title of the story. (optional)
    description = 'description_example' # str | A brief description of the story. (optional)
    narrator_voice_id = 56 # int | Specifies the identifier of the AI voice that will narrate the story. This voice selection determines the tone, accent, and delivery style used to bring the contents of the uploaded .txt or .docx file to life. (optional)
    chosen_dictionaries = [56] # List[int] | An optional list of dictionary IDs selected by the user. Each entry must be an integer corresponding to a valid dictionary ID. If provided, at least one ID is required. (optional)

    try:
        # Create Story
        api_response = api_instance.create_story(file, source_language, title=title, description=description, narrator_voice_id=narrator_voice_id, chosen_dictionaries=chosen_dictionaries)
        print("The response of StoriesApi->create_story:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StoriesApi->create_story: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **bytearray**| The text file (&#x60;.txt&#x60;) or Word document (&#x60;.docx&#x60;) that its contents will be used for creating a story. | 
 **source_language** | [**Languages**](Languages.md)| The language of the contents in the input file. | 
 **title** | **str**| The title of the story. | [optional] 
 **description** | **str**| A brief description of the story. | [optional] 
 **narrator_voice_id** | **int**| Specifies the identifier of the AI voice that will narrate the story. This voice selection determines the tone, accent, and delivery style used to bring the contents of the uploaded .txt or .docx file to life. | [optional] 
 **chosen_dictionaries** | [**List[int]**](int.md)| An optional list of dictionary IDs selected by the user. Each entry must be an integer corresponding to a valid dictionary ID. If provided, at least one ID is required. | [optional] 

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

# **create_translated_story**
> TaskID create_translated_story(run_id, create_translated_story_request_payload)

Create Translated Story

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
from cambai.models.create_translated_story_request_payload import CreateTranslatedStoryRequestPayload
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
    api_instance = cambai.StoriesApi(api_client)
    run_id = 56 # int | 
    create_translated_story_request_payload = cambai.CreateTranslatedStoryRequestPayload() # CreateTranslatedStoryRequestPayload | 

    try:
        # Create Translated Story
        api_response = api_instance.create_translated_story(run_id, create_translated_story_request_payload)
        print("The response of StoriesApi->create_translated_story:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StoriesApi->create_translated_story: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **run_id** | **int**|  | 
 **create_translated_story_request_payload** | [**CreateTranslatedStoryRequestPayload**](CreateTranslatedStoryRequestPayload.md)|  | 

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

# **get_story_run_info_by_id**
> StoryRunInfoResponse get_story_run_info_by_id(run_id, include_transcript=include_transcript)

Get Story Run Info

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
from cambai.models.story_run_info_response import StoryRunInfoResponse
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
    api_instance = cambai.StoriesApi(api_client)
    run_id = 56 # int | 
    include_transcript = False # bool |  (optional) (default to False)

    try:
        # Get Story Run Info
        api_response = api_instance.get_story_run_info_by_id(run_id, include_transcript=include_transcript)
        print("The response of StoriesApi->get_story_run_info_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StoriesApi->get_story_run_info_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **run_id** | **int**|  | 
 **include_transcript** | **bool**|  | [optional] [default to False]

### Return type

[**StoryRunInfoResponse**](StoryRunInfoResponse.md)

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_translated_story_run_info**
> StoryRunInfoResponse get_translated_story_run_info(run_id, target_language, include_transcript=include_transcript)

Get Translated Story Run Info

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
from cambai.models.languages import Languages
from cambai.models.story_run_info_response import StoryRunInfoResponse
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
    api_instance = cambai.StoriesApi(api_client)
    run_id = 56 # int | 
    target_language = cambai.Languages() # Languages | 
    include_transcript = False # bool |  (optional) (default to False)

    try:
        # Get Translated Story Run Info
        api_response = api_instance.get_translated_story_run_info(run_id, target_language, include_transcript=include_transcript)
        print("The response of StoriesApi->get_translated_story_run_info:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StoriesApi->get_translated_story_run_info: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **run_id** | **int**|  | 
 **target_language** | [**Languages**](.md)|  | 
 **include_transcript** | **bool**|  | [optional] [default to False]

### Return type

[**StoryRunInfoResponse**](StoryRunInfoResponse.md)

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

# **get_translated_story_status_by_id**
> OrchestratorPipelineResult get_translated_story_status_by_id(task_id)

Get Translated Story Status

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
    api_instance = cambai.StoriesApi(api_client)
    task_id = 'task_id_example' # str | 

    try:
        # Get Translated Story Status
        api_response = api_instance.get_translated_story_status_by_id(task_id)
        print("The response of StoriesApi->get_translated_story_status_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StoriesApi->get_translated_story_status_by_id: %s\n" % e)
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

