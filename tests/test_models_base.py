"""
Tests for base model classes - aliexpress_async_api.models.base
"""
import pytest
from dataclasses import fields
from aliexpress_async_api.models.base import BaseModel


class TestBaseModel:
    """Base model tests"""
    
    def test_base_model_has_raw_data_field(self):
        """Test that BaseModel includes raw_data field"""
        model_fields = {f.name for f in fields(BaseModel)}
        assert "raw_data" in model_fields
    
    def test_base_model_raw_data_is_dict(self):
        """Test that raw_data field is a dict"""
        model = BaseModel(raw_data={"key": "value"})
        assert isinstance(model.raw_data, dict)
        assert model.raw_data["key"] == "value"
    
    def test_base_model_raw_data_default_empty_dict(self):
        """Test that raw_data defaults to empty dict"""
        model = BaseModel()
        assert isinstance(model.raw_data, dict)
        assert len(model.raw_data) == 0
    
    def test_base_model_is_dataclass(self):
        """Test that BaseModel is a proper dataclass"""
        from dataclasses import is_dataclass
        assert is_dataclass(BaseModel)
    
    def test_base_model_repr(self):
        """Test BaseModel string representation"""
        model = BaseModel(raw_data={"test": "data"})
        repr_str = repr(model)
        assert "BaseModel" in repr_str
        assert "raw_data" in repr_str
