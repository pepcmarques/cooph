import pytest

from coop.base.models import Cooperative  # noqa
from coop.base.models import Unit  # noqa


@pytest.mark.parametrize(
    "base_model, field_name, value", [
        ("Cooperative", "cooperative_name", "Cooperative Test - Model"),
        ("Unit", "unit_number", 12345),
    ]
)
def test_messaging_model_str(base_model, field_name, value):
    obj = eval(base_model)()
    obj.__dict__.update({field_name: value})
    assert str(obj) == str(value)


@pytest.mark.parametrize(
    "base_model, field_name, value", [
        ("Cooperative", "cooperative_name", "Cooperative Test - Model"),
    ]
)
def test_setting_cooperative_name(base_model, field_name, value):
    obj = eval(base_model)()
    obj.set_cooperative_name(value)
    assert str(obj) == str(value)
