# cambai.ApisApi

All URIs are relative to *https://client.camb.ai/apis*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_audio_separation**](ApisApi.md#create_audio_separation) | **POST** /audio-separation | Create Audio Separation
[**create_custom_voice**](ApisApi.md#create_custom_voice) | **POST** /create-custom-voice | Create Custom Voice
[**create_end_to_end_dubbing**](ApisApi.md#create_end_to_end_dubbing) | **POST** /dub | End To End Dubbing
[**create_story**](ApisApi.md#create_story) | **POST** /story | Create Story
[**create_text_to_sound**](ApisApi.md#create_text_to_sound) | **POST** /text-to-sound | Create Text to Sound
[**create_transcription**](ApisApi.md#create_transcription) | **POST** /transcribe | Create Transcription
[**create_translated_story**](ApisApi.md#create_translated_story) | **POST** /translated-story/{run_id} | Create Translated Story
[**create_translated_tts**](ApisApi.md#create_translated_tts) | **POST** /translated-tts | Create Translated Tts
[**create_translation**](ApisApi.md#create_translation) | **POST** /translate | Create Translation
[**create_translation_stream**](ApisApi.md#create_translation_stream) | **POST** /translation/stream | Create Translation Stream
[**create_tts**](ApisApi.md#create_tts) | **POST** /tts | Create Tts
[**create_voice_from_description**](ApisApi.md#create_voice_from_description) | **POST** /text-to-voice | Create Voice from Description
[**dictionaries_get**](ApisApi.md#dictionaries_get) | **GET** /dictionaries | Get Workspace Dictionaries
[**get_audio_separation_run_info_by_id**](ApisApi.md#get_audio_separation_run_info_by_id) | **GET** /audio-separation-result/{run_id} | Get Audio Separation Run Info
[**get_audio_separation_status_by_id**](ApisApi.md#get_audio_separation_status_by_id) | **GET** /audio-separation/{task_id} | Get Audio Separation Status
[**get_dubbed_run_info_by_id**](ApisApi.md#get_dubbed_run_info_by_id) | **GET** /dub-result/{run_id} | Get Dubbed Run Info
[**get_end_to_end_dubbing_status_by_id**](ApisApi.md#get_end_to_end_dubbing_status_by_id) | **GET** /dub/{task_id} | Get End To End Dubbing Status
[**get_source_languages**](ApisApi.md#get_source_languages) | **GET** /source-languages | Get Source Languages
[**get_story_run_info_by_id**](ApisApi.md#get_story_run_info_by_id) | **GET** /story-result/{run_id} | Get Story Run Info
[**get_story_status_by_id**](ApisApi.md#get_story_status_by_id) | **GET** /story/{task_id} | Get Story Status
[**get_target_languages**](ApisApi.md#get_target_languages) | **GET** /target-languages | Get Target Languages
[**get_text_to_audio_status_by_id**](ApisApi.md#get_text_to_audio_status_by_id) | **GET** /text-to-sound/{task_id} | Get Text To Audio Status
[**get_text_to_sound_run_result_by_id**](ApisApi.md#get_text_to_sound_run_result_by_id) | **GET** /text-to-sound-result/{run_id} | Get Text to Sound Run Result
[**get_text_to_voice_run_result_by_id**](ApisApi.md#get_text_to_voice_run_result_by_id) | **GET** /text-to-voice-result/{run_id} | Get Text-to-Voice Run Result
[**get_transcription_result_by_id**](ApisApi.md#get_transcription_result_by_id) | **GET** /transcription-result/{run_id} | Get Transcription Result
[**get_transcription_task_status_by_id**](ApisApi.md#get_transcription_task_status_by_id) | **GET** /transcribe/{task_id} | Create Transcription Task Status
[**get_translated_story_run_info**](ApisApi.md#get_translated_story_run_info) | **GET** /translated-story-result/{run_id}/{target_language} | Get Translated Story Run Info
[**get_translated_story_status_by_id**](ApisApi.md#get_translated_story_status_by_id) | **GET** /translated-story/{task_id} | Get Translated Story Status
[**get_translated_tts_task_status_by_id**](ApisApi.md#get_translated_tts_task_status_by_id) | **GET** /translated-tts/{task_id} | Create Translated Tts Task Status
[**get_translation_result_by_id**](ApisApi.md#get_translation_result_by_id) | **GET** /translation-result/{run_id} | Get Translation Result
[**get_translation_task_status_by_id**](ApisApi.md#get_translation_task_status_by_id) | **GET** /translate/{task_id} | Create translation Task Status
[**get_tts_result_by_id**](ApisApi.md#get_tts_result_by_id) | **GET** /tts/{id} | Get Tts Result
[**get_tts_run_info_by_id**](ApisApi.md#get_tts_run_info_by_id) | **GET** /tts-result/{run_id} | Get Tts Run Info
[**list_voices**](ApisApi.md#list_voices) | **GET** /list-voices | List Voices
[**text_to_voice_task_id_get**](ApisApi.md#text_to_voice_task_id_get) | **GET** /text-to-voice/{task_id} | Get Text-to-Voice Task Status


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
    api_instance = cambai.ApisApi(api_client)
    audio_file = None # bytearray | Media file to processed. AAC, FLAC, MP3 and WAV formats are supported. (optional)

    try:
        # Create Audio Separation
        api_response = api_instance.create_audio_separation(audio_file=audio_file)
        print("The response of ApisApi->create_audio_separation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->create_audio_separation: %s\n" % e)
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

# **create_custom_voice**
> CreateCustomVoiceOut create_custom_voice(voice_name, gender, file, description=description, publish_voice_to_market_place=publish_voice_to_market_place, age=age, enhance_audio=enhance_audio, language=language)

Create Custom Voice

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
from cambai.models.create_custom_voice_out import CreateCustomVoiceOut
from cambai.models.gender import Gender
from cambai.models.languages import Languages
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
    api_instance = cambai.ApisApi(api_client)
    voice_name = 'voice_name_example' # str | The name or label to be assigned to the voice.
    gender = cambai.Gender() # Gender | Represents the gender of the speaker in the provided audio. Values are encoded as integers.
    file = None # bytearray | The reference audio file that will be used to create the custom voice. The file should have clear speech to ensure optimal cloning accuracy. Supported formats include `.aac`, `.flac`, `.mp3` and `.wav`.
    description = 'description_example' # str | A brief summary of the custom voice—e.g. its intended use, tone or character traits. (optional)
    publish_voice_to_market_place = True # bool | Set this to `true` to publish this custom voice to the marketplace for others to use. By making it available in the marketplace you consent to the guidelines and terms & conditions. (optional)
    age = 30 # int | The estimated or actual age of the speaker in the reference audio. (optional) (default to 30)
    enhance_audio = False # bool | If set to `true`, the system will apply audio enhancement techniques such as noise reduction and volume normalization to improve voice clarity. (optional) (default to False)
    language = cambai.Languages() # Languages | The language of the reference audio file. This field is optional. (optional)

    try:
        # Create Custom Voice
        api_response = api_instance.create_custom_voice(voice_name, gender, file, description=description, publish_voice_to_market_place=publish_voice_to_market_place, age=age, enhance_audio=enhance_audio, language=language)
        print("The response of ApisApi->create_custom_voice:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->create_custom_voice: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **voice_name** | **str**| The name or label to be assigned to the voice. | 
 **gender** | [**Gender**](Gender.md)| Represents the gender of the speaker in the provided audio. Values are encoded as integers. | 
 **file** | **bytearray**| The reference audio file that will be used to create the custom voice. The file should have clear speech to ensure optimal cloning accuracy. Supported formats include &#x60;.aac&#x60;, &#x60;.flac&#x60;, &#x60;.mp3&#x60; and &#x60;.wav&#x60;. | 
 **description** | **str**| A brief summary of the custom voice—e.g. its intended use, tone or character traits. | [optional] 
 **publish_voice_to_market_place** | **bool**| Set this to &#x60;true&#x60; to publish this custom voice to the marketplace for others to use. By making it available in the marketplace you consent to the guidelines and terms &amp; conditions. | [optional] 
 **age** | **int**| The estimated or actual age of the speaker in the reference audio. | [optional] [default to 30]
 **enhance_audio** | **bool**| If set to &#x60;true&#x60;, the system will apply audio enhancement techniques such as noise reduction and volume normalization to improve voice clarity. | [optional] [default to False]
 **language** | [**Languages**](Languages.md)| The language of the reference audio file. This field is optional. | [optional] 

### Return type

[**CreateCustomVoiceOut**](CreateCustomVoiceOut.md)

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

# **create_end_to_end_dubbing**
> TaskID create_end_to_end_dubbing(end_to_end_dubbing_request_payload)

End To End Dubbing

Initiate a full end to end dubbing task.

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
from cambai.models.end_to_end_dubbing_request_payload import EndToEndDubbingRequestPayload
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
    api_instance = cambai.ApisApi(api_client)
    end_to_end_dubbing_request_payload = cambai.EndToEndDubbingRequestPayload() # EndToEndDubbingRequestPayload | 

    try:
        # End To End Dubbing
        api_response = api_instance.create_end_to_end_dubbing(end_to_end_dubbing_request_payload)
        print("The response of ApisApi->create_end_to_end_dubbing:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->create_end_to_end_dubbing: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **end_to_end_dubbing_request_payload** | [**EndToEndDubbingRequestPayload**](EndToEndDubbingRequestPayload.md)|  | 

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
    api_instance = cambai.ApisApi(api_client)
    file = None # bytearray | The text file (`.txt`) or Word document (`.docx`) that its contents will be used for creating a story.
    source_language = cambai.Languages() # Languages | The language of the contents in the input file.
    title = 'title_example' # str | The title of the story. (optional)
    description = 'description_example' # str | A brief description of the story. (optional)
    narrator_voice_id = 56 # int | Specifies the identifier of the AI voice that will narrate the story. This voice selection determines the tone, accent, and delivery style used to bring the contents of the uploaded .txt or .docx file to life. (optional)
    chosen_dictionaries = [56] # List[int] | An optional list of dictionary IDs selected by the user. Each entry must be an integer corresponding to a valid dictionary ID. If provided, at least one ID is required. (optional)

    try:
        # Create Story
        api_response = api_instance.create_story(file, source_language, title=title, description=description, narrator_voice_id=narrator_voice_id, chosen_dictionaries=chosen_dictionaries)
        print("The response of ApisApi->create_story:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->create_story: %s\n" % e)
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
    api_instance = cambai.ApisApi(api_client)
    create_text_to_audio_request_payload = cambai.CreateTextToAudioRequestPayload() # CreateTextToAudioRequestPayload | 

    try:
        # Create Text to Sound
        api_response = api_instance.create_text_to_sound(create_text_to_audio_request_payload)
        print("The response of ApisApi->create_text_to_sound:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->create_text_to_sound: %s\n" % e)
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

# **create_transcription**
> TaskID create_transcription(language, file)

Create Transcription

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
    api_instance = cambai.ApisApi(api_client)
    language = cambai.Languages() # Languages | 
    file = None # bytearray | Media file for transcription

    try:
        # Create Transcription
        api_response = api_instance.create_transcription(language, file)
        print("The response of ApisApi->create_transcription:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->create_transcription: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **language** | [**Languages**](Languages.md)|  | 
 **file** | **bytearray**| Media file for transcription | 

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
    api_instance = cambai.ApisApi(api_client)
    run_id = 56 # int | 
    create_translated_story_request_payload = cambai.CreateTranslatedStoryRequestPayload() # CreateTranslatedStoryRequestPayload | 

    try:
        # Create Translated Story
        api_response = api_instance.create_translated_story(run_id, create_translated_story_request_payload)
        print("The response of ApisApi->create_translated_story:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->create_translated_story: %s\n" % e)
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

# **create_translated_tts**
> object create_translated_tts(create_translated_tts_request_payload, run_id=run_id)

Create Translated Tts

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
from cambai.models.create_translated_tts_request_payload import CreateTranslatedTTSRequestPayload
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
    api_instance = cambai.ApisApi(api_client)
    create_translated_tts_request_payload = cambai.CreateTranslatedTTSRequestPayload() # CreateTranslatedTTSRequestPayload | 
    run_id = 56 # int |  (optional)

    try:
        # Create Translated Tts
        api_response = api_instance.create_translated_tts(create_translated_tts_request_payload, run_id=run_id)
        print("The response of ApisApi->create_translated_tts:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->create_translated_tts: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_translated_tts_request_payload** | [**CreateTranslatedTTSRequestPayload**](CreateTranslatedTTSRequestPayload.md)|  | 
 **run_id** | **int**|  | [optional] 

### Return type

**object**

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

# **create_translation**
> TaskID create_translation(body_translate_translate_post)

Create Translation

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
from cambai.models.body_translate_translate_post import BodyTranslateTranslatePost
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
    api_instance = cambai.ApisApi(api_client)
    body_translate_translate_post = cambai.BodyTranslateTranslatePost() # BodyTranslateTranslatePost | 

    try:
        # Create Translation
        api_response = api_instance.create_translation(body_translate_translate_post)
        print("The response of ApisApi->create_translation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->create_translation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body_translate_translate_post** | [**BodyTranslateTranslatePost**](BodyTranslateTranslatePost.md)|  | 

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

# **create_translation_stream**
> str create_translation_stream(create_translation_stream_request_payload)

Create Translation Stream

Stream real-time text translation between languages

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
from cambai.models.create_translation_stream_request_payload import CreateTranslationStreamRequestPayload
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
    api_instance = cambai.ApisApi(api_client)
    create_translation_stream_request_payload = cambai.CreateTranslationStreamRequestPayload() # CreateTranslationStreamRequestPayload | 

    try:
        # Create Translation Stream
        api_response = api_instance.create_translation_stream(create_translation_stream_request_payload)
        print("The response of ApisApi->create_translation_stream:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->create_translation_stream: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_translation_stream_request_payload** | [**CreateTranslationStreamRequestPayload**](CreateTranslationStreamRequestPayload.md)|  | 

### Return type

**str**

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/event-stream, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Text translation stream |  * X-Credits-Required -  <br>  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

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
    api_instance = cambai.ApisApi(api_client)
    create_tts_request_payload = cambai.CreateTTSRequestPayload() # CreateTTSRequestPayload | 

    try:
        # Create Tts
        api_response = api_instance.create_tts(create_tts_request_payload)
        print("The response of ApisApi->create_tts:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->create_tts: %s\n" % e)
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

# **create_tts_stream**
> bytearray create_tts_stream(create_tts_stream_request_payload)

Create TTS Stream

Stream text-to-speech audio in real-time

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
from cambai.models.create_tts_stream_request_payload import CreateTTSStreamRequestPayload
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
    api_instance = cambai.ApisApi(api_client)
    create_tts_stream_request_payload = cambai.CreateTTSStreamRequestPayload() # CreateTTSStreamRequestPayload | 

    try:
        # Create TTS Stream
        api_response = api_instance.create_tts_stream(create_tts_stream_request_payload)
        print("The response of ApisApi->create_tts_stream:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->create_tts_stream: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_tts_stream_request_payload** | [**CreateTTSStreamRequestPayload**](CreateTTSStreamRequestPayload.md)|  | 

### Return type

**bytearray**

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: audio/flac, audio/wav, audio/aac, audio/x-pcm, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Generated speech audio in the specified format. |  * X-Credits-Required -  <br>  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

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
    api_instance = cambai.ApisApi(api_client)
    create_text_to_voice_request_payload = cambai.CreateTextToVoiceRequestPayload() # CreateTextToVoiceRequestPayload | 

    try:
        # Create Voice from Description
        api_response = api_instance.create_voice_from_description(create_text_to_voice_request_payload)
        print("The response of ApisApi->create_voice_from_description:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->create_voice_from_description: %s\n" % e)
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
    api_instance = cambai.ApisApi(api_client)

    try:
        # Get Workspace Dictionaries
        api_response = api_instance.dictionaries_get()
        print("The response of ApisApi->dictionaries_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->dictionaries_get: %s\n" % e)
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
    api_instance = cambai.ApisApi(api_client)
    run_id = 56 # int | 

    try:
        # Get Audio Separation Run Info
        api_response = api_instance.get_audio_separation_run_info_by_id(run_id)
        print("The response of ApisApi->get_audio_separation_run_info_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->get_audio_separation_run_info_by_id: %s\n" % e)
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
    api_instance = cambai.ApisApi(api_client)
    task_id = 'task_id_example' # str | 

    try:
        # Get Audio Separation Status
        api_response = api_instance.get_audio_separation_status_by_id(task_id)
        print("The response of ApisApi->get_audio_separation_status_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->get_audio_separation_status_by_id: %s\n" % e)
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

# **get_dubbed_run_info_by_id**
> RunInfoResponse get_dubbed_run_info_by_id(run_id)

Get Dubbed Run Info



### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
from cambai.models.run_info_response import RunInfoResponse
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
    api_instance = cambai.ApisApi(api_client)
    run_id = 56 # int | The unique identifier for the run, which was generated during the end to end dub creation process and returned upon task completion.

    try:
        # Get Dubbed Run Info
        api_response = api_instance.get_dubbed_run_info_by_id(run_id)
        print("The response of ApisApi->get_dubbed_run_info_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->get_dubbed_run_info_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **run_id** | **int**| The unique identifier for the run, which was generated during the end to end dub creation process and returned upon task completion. | 

### Return type

[**RunInfoResponse**](RunInfoResponse.md)

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

# **get_end_to_end_dubbing_status_by_id**
> OrchestratorPipelineResult get_end_to_end_dubbing_status_by_id(task_id)

Get End To End Dubbing Status

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
    api_instance = cambai.ApisApi(api_client)
    task_id = 'task_id_example' # str | 

    try:
        # Get End To End Dubbing Status
        api_response = api_instance.get_end_to_end_dubbing_status_by_id(task_id)
        print("The response of ApisApi->get_end_to_end_dubbing_status_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->get_end_to_end_dubbing_status_by_id: %s\n" % e)
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

# **get_source_languages**
> List[LanguageItem] get_source_languages()

Get Source Languages

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
from cambai.models.language_item import LanguageItem
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
    api_instance = cambai.ApisApi(api_client)

    try:
        # Get Source Languages
        api_response = api_instance.get_source_languages()
        print("The response of ApisApi->get_source_languages:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->get_source_languages: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[LanguageItem]**](LanguageItem.md)

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
    api_instance = cambai.ApisApi(api_client)
    run_id = 56 # int | 
    include_transcript = False # bool |  (optional) (default to False)

    try:
        # Get Story Run Info
        api_response = api_instance.get_story_run_info_by_id(run_id, include_transcript=include_transcript)
        print("The response of ApisApi->get_story_run_info_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->get_story_run_info_by_id: %s\n" % e)
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

# **get_story_status_by_id**
> OrchestratorPipelineResult get_story_status_by_id(task_id)

Get Story Status

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
    api_instance = cambai.ApisApi(api_client)
    task_id = 'task_id_example' # str | 

    try:
        # Get Story Status
        api_response = api_instance.get_story_status_by_id(task_id)
        print("The response of ApisApi->get_story_status_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->get_story_status_by_id: %s\n" % e)
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

# **get_target_languages**
> List[LanguageItem] get_target_languages()

Get Target Languages

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
from cambai.models.language_item import LanguageItem
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
    api_instance = cambai.ApisApi(api_client)

    try:
        # Get Target Languages
        api_response = api_instance.get_target_languages()
        print("The response of ApisApi->get_target_languages:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->get_target_languages: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[LanguageItem]**](LanguageItem.md)

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
    api_instance = cambai.ApisApi(api_client)
    task_id = 'task_id_example' # str | 

    try:
        # Get Text To Audio Status
        api_response = api_instance.get_text_to_audio_status_by_id(task_id)
        print("The response of ApisApi->get_text_to_audio_status_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->get_text_to_audio_status_by_id: %s\n" % e)
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
    api_instance = cambai.ApisApi(api_client)
    run_id = 56 # int | The unique identifier for the run, which was generated during the text to an audio effect creation process and returned upon task completion.

    try:
        # Get Text to Sound Run Result
        api_response = api_instance.get_text_to_sound_run_result_by_id(run_id)
        print("The response of ApisApi->get_text_to_sound_run_result_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->get_text_to_sound_run_result_by_id: %s\n" % e)
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
    api_instance = cambai.ApisApi(api_client)
    run_id = 56 # int | The unique identifier for the run, which was generated during the text to voice creation process and returned upon task completion.

    try:
        # Get Text-to-Voice Run Result
        api_response = api_instance.get_text_to_voice_run_result_by_id(run_id)
        print("The response of ApisApi->get_text_to_voice_run_result_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->get_text_to_voice_run_result_by_id: %s\n" % e)
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

# **get_transcription_result_by_id**
> List[DialogueItem] get_transcription_result_by_id(run_id, word_level_timestamps=word_level_timestamps)

Get Transcription Result

Get the result for your transcription only project by using the run_id

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
from cambai.models.dialogue_item import DialogueItem
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
    api_instance = cambai.ApisApi(api_client)
    run_id = 56 # int | The unique identifier for the run, which was generated during the transcription creation process and returned upon task completion.
    word_level_timestamps = False # bool |  (optional) (default to False)

    try:
        # Get Transcription Result
        api_response = api_instance.get_transcription_result_by_id(run_id, word_level_timestamps=word_level_timestamps)
        print("The response of ApisApi->get_transcription_result_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->get_transcription_result_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **run_id** | **int**| The unique identifier for the run, which was generated during the transcription creation process and returned upon task completion. | 
 **word_level_timestamps** | **bool**|  | [optional] [default to False]

### Return type

[**List[DialogueItem]**](DialogueItem.md)

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

# **get_transcription_task_status_by_id**
> OrchestratorPipelineResult get_transcription_task_status_by_id(task_id)

Create Transcription Task Status

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
    api_instance = cambai.ApisApi(api_client)
    task_id = 'task_id_example' # str | 

    try:
        # Create Transcription Task Status
        api_response = api_instance.get_transcription_task_status_by_id(task_id)
        print("The response of ApisApi->get_transcription_task_status_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->get_transcription_task_status_by_id: %s\n" % e)
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
    api_instance = cambai.ApisApi(api_client)
    run_id = 56 # int | 
    target_language = cambai.Languages() # Languages | 
    include_transcript = False # bool |  (optional) (default to False)

    try:
        # Get Translated Story Run Info
        api_response = api_instance.get_translated_story_run_info(run_id, target_language, include_transcript=include_transcript)
        print("The response of ApisApi->get_translated_story_run_info:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->get_translated_story_run_info: %s\n" % e)
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
    api_instance = cambai.ApisApi(api_client)
    task_id = 'task_id_example' # str | 

    try:
        # Get Translated Story Status
        api_response = api_instance.get_translated_story_status_by_id(task_id)
        print("The response of ApisApi->get_translated_story_status_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->get_translated_story_status_by_id: %s\n" % e)
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

# **get_translated_tts_task_status_by_id**
> OrchestratorPipelineResult get_translated_tts_task_status_by_id(task_id)

Create Translated Tts Task Status

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
    api_instance = cambai.ApisApi(api_client)
    task_id = 'task_id_example' # str | 

    try:
        # Create Translated Tts Task Status
        api_response = api_instance.get_translated_tts_task_status_by_id(task_id)
        print("The response of ApisApi->get_translated_tts_task_status_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->get_translated_tts_task_status_by_id: %s\n" % e)
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

# **get_translation_result_by_id**
> TranslationResult get_translation_result_by_id(run_id)

Get Translation Result

Get the result for your translation only project by using the run_id

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
from cambai.models.translation_result import TranslationResult
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
    api_instance = cambai.ApisApi(api_client)
    run_id = 56 # int | The unique identifier for the run, which was generated during the translation creation process and returned upon task completion.

    try:
        # Get Translation Result
        api_response = api_instance.get_translation_result_by_id(run_id)
        print("The response of ApisApi->get_translation_result_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->get_translation_result_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **run_id** | **int**| The unique identifier for the run, which was generated during the translation creation process and returned upon task completion. | 

### Return type

[**TranslationResult**](TranslationResult.md)

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

# **get_translation_task_status_by_id**
> OrchestratorPipelineResult get_translation_task_status_by_id(task_id)

Create translation Task Status

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
    api_instance = cambai.ApisApi(api_client)
    task_id = 'task_id_example' # str | 

    try:
        # Create translation Task Status
        api_response = api_instance.get_translation_task_status_by_id(task_id)
        print("The response of ApisApi->get_translation_task_status_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->get_translation_task_status_by_id: %s\n" % e)
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
    api_instance = cambai.ApisApi(api_client)
    id = 'id_example' # str | 

    try:
        # Get Tts Result
        api_response = api_instance.get_tts_result_by_id(id)
        print("The response of ApisApi->get_tts_result_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->get_tts_result_by_id: %s\n" % e)
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

# **get_tts_run_info_by_id**
> str get_tts_run_info_by_id(run_id, output_type=output_type)

Get Tts Run Info

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
from cambai.models.output_type import OutputType
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
    api_instance = cambai.ApisApi(api_client)
    run_id = 56 # int | 
    output_type = raw_bytes # OutputType | The type of the Text-to-Speech output to return. Either streamable audio bytes or a URL to the generated file. (optional) (default to raw_bytes)

    try:
        # Get Tts Run Info
        api_response = api_instance.get_tts_run_info_by_id(run_id, output_type=output_type)
        print("The response of ApisApi->get_tts_run_info_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->get_tts_run_info_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **run_id** | **int**|  | 
 **output_type** | [**OutputType**](.md)| The type of the Text-to-Speech output to return. Either streamable audio bytes or a URL to the generated file. | [optional] [default to raw_bytes]

### Return type

**str**

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: audio/flac, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_voices**
> List[VoiceItem] list_voices()

List Voices

### Example

* Api Key Authentication (APIKeyHeader):

```python
import cambai
from cambai.models.voice_item import VoiceItem
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
    api_instance = cambai.ApisApi(api_client)

    try:
        # List Voices
        api_response = api_instance.list_voices()
        print("The response of ApisApi->list_voices:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->list_voices: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[VoiceItem]**](VoiceItem.md)

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
    api_instance = cambai.ApisApi(api_client)
    task_id = 'task_id_example' # str | 

    try:
        # Get Text-to-Voice Task Status
        api_response = api_instance.text_to_voice_task_id_get(task_id)
        print("The response of ApisApi->text_to_voice_task_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApisApi->text_to_voice_task_id_get: %s\n" % e)
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

