from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, Optional
from typing import Optional, Set
from typing_extensions import Self

class OutputConfiguration(BaseModel):
    """
    OutputConfiguration - Configuration for audio output format and processing.
    """ # noqa: E501
    format: Optional[str] = Field(default=None, description="The output audio format (e.g., 'mp3', 'wav', 'flac', 'aac').")
    duration: Optional[float] = Field(default=None, description="The desired duration of the output audio in seconds. If null, the duration will be determined by the input text.")
    apply_enhancement: Optional[bool] = Field(default=None, description="Whether to apply audio enhancement techniques such as noise reduction and normalization.")
    __properties: ClassVar[List[str]] = ["format", "duration", "apply_enhancement"]

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
        """Create an instance of OutputConfiguration from a JSON string"""
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
        """Create an instance of OutputConfiguration from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "format": obj.get("format"),
            "duration": obj.get("duration"),
            "apply_enhancement": obj.get("apply_enhancement")
        })
        return _obj
