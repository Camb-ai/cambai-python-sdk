# StoryRunInfoResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**audio_url** | **str** | The URL pointing to the generated audio file for the story. | [optional] 
**dialogue_url** | **str** | The URL pointing to the audio file that contains the story&#39;s dialogue. | [optional] 
**transcript** | [**List[DialogueItem]**](DialogueItem.md) | A collection of dialogue items representing the textual transcript of the story. | [optional] 

## Example

```python
from cambai.models.story_run_info_response import StoryRunInfoResponse

# TODO update the JSON string below
json = "{}"
# create an instance of StoryRunInfoResponse from a JSON string
story_run_info_response_instance = StoryRunInfoResponse.from_json(json)
# print the JSON string representation of the object
print(StoryRunInfoResponse.to_json())

# convert the object into a dict
story_run_info_response_dict = story_run_info_response_instance.to_dict()
# create an instance of StoryRunInfoResponse from a dict
story_run_info_response_from_dict = StoryRunInfoResponse.from_dict(story_run_info_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


