# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# License: MIT

import frappe
import pytest
from databridge.utils.validators import validate_required, validate_max_length


class TestValidateRequired:
    def test_raises_on_empty_string(self):
        with pytest.raises(frappe.ValidationError):
            validate_required("", "Field Name")

    def test_raises_on_none(self):
        with pytest.raises(frappe.ValidationError):
            validate_required(None, "Field Name")

    def test_passes_on_valid_value(self):
        validate_required("hello", "Field Name")

    def test_passes_on_number(self):
        validate_required(42, "Field Name")


class TestValidateMaxLength:
    def test_raises_on_too_long(self):
        with pytest.raises(frappe.ValidationError):
            validate_max_length("x" * 150, 140, "Field Name")

    def test_passes_on_exact_length(self):
        validate_max_length("x" * 140, 140, "Field Name")

    def test_passes_on_short_string(self):
        validate_max_length("hello", 140, "Field Name")

    def test_passes_on_none(self):
        validate_max_length(None, 140, "Field Name")
