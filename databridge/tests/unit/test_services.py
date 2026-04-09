# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# License: MIT

import frappe
import pytest
from databridge.services.validation_service import ValidationService
from databridge.services.mapping_service import MappingService


class TestValidationServiceDetectDuplicates:
    """Test duplicate detection (pure logic, no DB needed)."""

    def test_no_duplicates(self):
        data = [
            {"customer_name": "Alice", "email": "alice@test.com"},
            {"customer_name": "Bob", "email": "bob@test.com"},
        ]
        result = ValidationService.detect_duplicates(data, "Customer", ["customer_name"])
        assert result == []

    def test_finds_exact_duplicate(self):
        data = [
            {"customer_name": "Alice"},
            {"customer_name": "Bob"},
            {"customer_name": "Alice"},
        ]
        result = ValidationService.detect_duplicates(data, "Customer", ["customer_name"])
        assert len(result) == 1
        assert result[0]["row"] == 3
        assert result[0]["duplicate_of_row"] == 1

    def test_case_insensitive_match(self):
        data = [
            {"customer_name": "Alice"},
            {"customer_name": "alice"},
        ]
        result = ValidationService.detect_duplicates(data, "Customer", ["customer_name"])
        assert len(result) == 1

    def test_multi_field_key(self):
        data = [
            {"name": "Alice", "city": "Dubai"},
            {"name": "Alice", "city": "Riyadh"},
            {"name": "Alice", "city": "Dubai"},
        ]
        result = ValidationService.detect_duplicates(data, "Customer", ["name", "city"])
        assert len(result) == 1
        assert result[0]["row"] == 3

    def test_empty_data(self):
        result = ValidationService.detect_duplicates([], "Customer", ["name"])
        assert result == []


class TestMappingServiceAutoMap:
    """Test field auto-mapping logic."""

    def test_exact_match(self):
        result = MappingService.auto_map_fields(["customer_name", "email_id"], "Customer")
        mapped_targets = [m["target_field"] for m in result]
        assert "customer_name" in mapped_targets

    def test_no_match_returns_empty(self):
        result = MappingService.auto_map_fields(["xyz_nonexistent_field_123"], "Customer")
        assert result == []

    def test_confidence_score(self):
        result = MappingService.auto_map_fields(["customer_name"], "Customer")
        if result:
            assert result[0]["confidence"] >= 0.9
