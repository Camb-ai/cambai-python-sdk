# BodyTranslateTranslatePost


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**source_language** | [**Languages**](Languages.md) |  | 
**target_language** | [**Languages**](Languages.md) |  | 
**texts** | **List[str]** |  | 
**age** | **int** |  | [optional] 
**formality** | [**Formalities**](Formalities.md) | Specifies whether the translated text should be formal or informal. For example, &#x60;1&#x60; (formal) may use polite language, while &#x60;2&#x60; (informal) may use casual or colloquial language. | [optional] 
**gender** | [**Gender**](Gender.md) |  | [optional] 
**chosen_dictionaries** | **List[int]** | An optional list of dictionary IDs selected by the user. Each entry must be an integer corresponding to a valid dictionary ID. If provided, at least one ID is required. | [optional] 

## Example

```python
from cambai.models.body_translate_translate_post import BodyTranslateTranslatePost

# TODO update the JSON string below
json = "{}"
# create an instance of BodyTranslateTranslatePost from a JSON string
body_translate_translate_post_instance = BodyTranslateTranslatePost.from_json(json)
# print the JSON string representation of the object
print(BodyTranslateTranslatePost.to_json())

# convert the object into a dict
body_translate_translate_post_dict = body_translate_translate_post_instance.to_dict()
# create an instance of BodyTranslateTranslatePost from a dict
body_translate_translate_post_from_dict = BodyTranslateTranslatePost.from_dict(body_translate_translate_post_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


