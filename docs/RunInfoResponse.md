# RunInfoResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**run_id** | **int** | The unique identifier for the run, which was generated during the end to end dub creation process and returned upon task completion. | [optional] 
**output_video_url** | **str** | The URL pointing to the generated dubbed video file. | [optional] 
**output_audio_url** | **str** | The URL pointing to the generated dubbed audio file. | [optional] 
**transcript** | [**List[DialogueItem]**](DialogueItem.md) | A collection of dialogue items representing the textual transcript of the dubbed output. | [optional] 

## Example

```python
from cambai.models.run_info_response import RunInfoResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RunInfoResponse from a JSON string
run_info_response_instance = RunInfoResponse.from_json(json)
# print the JSON string representation of the object
print(RunInfoResponse.to_json())

# convert the object into a dict
run_info_response_dict = run_info_response_instance.to_dict()
# create an instance of RunInfoResponse from a dict
run_info_response_from_dict = RunInfoResponse.from_dict(run_info_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


