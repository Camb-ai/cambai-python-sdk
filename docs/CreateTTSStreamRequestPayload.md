# CreateTTSStreamRequestPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**text** | **str** | The content you want converted into spoken audio. This can be anything from a single sentence to paragraphs of text, supporting punctuation for natural speech patterns. | 
**voice_id** | **int** | The unique identifier for your selected voice profile. You can obtain available voice IDs from the &#x60;/list-voices&#x60; endpoint or create custom voices with the &#x60;/create-custom-voice&#x60; endpoint. | 
**language** | [**Languages**](Languages.md) | The source language of your input text. This helps the system apply the correct pronunciation rules and speech patterns. | 
**gender** | [**Gender**](Gender.md) | The preferred gender characteristics of the synthesized voice (&#x60;0 &#x3D; Not Specified, 1 &#x3D; Male, 2 &#x3D; Female, 9 &#x3D; Not Applicable&#x60;). Defaults to &#x60;null&#x60;. | [optional] 
**age** | **int** | The approximate age (between 1-100 years) to be reflected in the voice characteristics. This parameter helps fine-tune the timbre and speech patterns to match different age groups. | [optional] 
**output_format** | [**TTSStreamOutputFormat**](TTSStreamOutputFormat.md) | The audio file format for the generated speech stream. | [optional] 

## Example

```python
from cambai.models.create_tts_stream_request_payload import CreateTTSStreamRequestPayload

# TODO update the JSON string below
json = "{}"
# create an instance of CreateTTSStreamRequestPayload from a JSON string
create_tts_stream_request_payload_instance = CreateTTSStreamRequestPayload.from_json(json)
# print the JSON string representation of the object
print(CreateTTSStreamRequestPayload.to_json())

# convert the object into a dict
create_tts_stream_request_payload_dict = create_tts_stream_request_payload_instance.to_dict()
# create an instance of CreateTTSStreamRequestPayload from a dict
create_tts_stream_request_payload_from_dict = CreateTTSStreamRequestPayload.from_dict(create_tts_stream_request_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


