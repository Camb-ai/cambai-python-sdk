# EndToEndDubbingRequestPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**video_url** | **str** | The URL of the media file to be used to create the end-to-end dubbing task. | 
**source_language** | [**Languages**](Languages.md) | The original language of the media file to be used to create the end-to-end dubbing task. | 
**target_languages** | [**List[Languages]**](Languages.md) | The list of desired languages that the media file will be dubbed to. | [optional] 
**selected_audio_tracks** | **List[Optional[int]]** | Optional array of one or two zero‑based audio track indices to dub. Only supported for &#x60;MXF&#x60; files. If omitted, the first audio track (index 0) is used by default. | [optional] 
**add_output_as_an_audio_track** | **bool** | Optional flag to append the dubbed audio as a new audio track in the output file. Only supported for &#x60;MXF&#x60; files. If &#x60;true&#x60;, the dubbed audio is added as an additional track; if &#x60;false&#x60; or omitted, the source would be returned with only dubbed audio. | [optional] 
**chosen_dictionaries** | **List[int]** | An optional list of dictionary IDs selected by the user. Each entry must be an integer corresponding to a valid dictionary ID. If provided, at least one ID is required. | [optional] 

## Example

```python
from cambai.models.end_to_end_dubbing_request_payload import EndToEndDubbingRequestPayload

# TODO update the JSON string below
json = "{}"
# create an instance of EndToEndDubbingRequestPayload from a JSON string
end_to_end_dubbing_request_payload_instance = EndToEndDubbingRequestPayload.from_json(json)
# print the JSON string representation of the object
print(EndToEndDubbingRequestPayload.to_json())

# convert the object into a dict
end_to_end_dubbing_request_payload_dict = end_to_end_dubbing_request_payload_instance.to_dict()
# create an instance of EndToEndDubbingRequestPayload from a dict
end_to_end_dubbing_request_payload_from_dict = EndToEndDubbingRequestPayload.from_dict(end_to_end_dubbing_request_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


