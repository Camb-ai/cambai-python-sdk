# OrchestratorPipelineResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | [**TaskStatus**](TaskStatus.md) |  | [optional] 
**run_id** | **int** |  | [optional] 

## Example

```python
from cambai.models.orchestrator_pipeline_result import OrchestratorPipelineResult

# TODO update the JSON string below
json = "{}"
# create an instance of OrchestratorPipelineResult from a JSON string
orchestrator_pipeline_result_instance = OrchestratorPipelineResult.from_json(json)
# print the JSON string representation of the object
print(OrchestratorPipelineResult.to_json())

# convert the object into a dict
orchestrator_pipeline_result_dict = orchestrator_pipeline_result_instance.to_dict()
# create an instance of OrchestratorPipelineResult from a dict
orchestrator_pipeline_result_from_dict = OrchestratorPipelineResult.from_dict(orchestrator_pipeline_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


