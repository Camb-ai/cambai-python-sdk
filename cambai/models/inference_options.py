from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, Optional
from typing import Optional, Set
from typing_extensions import Self

class InferenceOptions(BaseModel):
    """
    InferenceOptions - Configuration for inference behavior and model parameters.
    """ # noqa: E501
    stability: Optional[float] = Field(default=None, description="Stability parameter for inference (0.0-1.0). Controls the consistency of the generated speech.")
    temperature: Optional[float] = Field(default=None, description="Temperature parameter for inference (0.0-1.0). Controls the randomness/creativity of the output.")
    inference_steps: Optional[int] = Field(default=None, description="Number of inference steps to perform. Higher values may produce better quality but take longer.")
    speaker_similarity: Optional[float] = Field(default=None, description="Speaker similarity score (0.0-1.0). Controls how closely the output matches the reference speaker.")
    __properties: ClassVar[List[str]] = ["stability", "temperature", "inference_steps", "speaker_similarity"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of InferenceOptions from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of InferenceOptions from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "stability": obj.get("stability"),
            "temperature": obj.get("temperature"),
            "inference_steps": obj.get("inference_steps"),
            "speaker_similarity": obj.get("speaker_similarity")
        })
        return _obj
