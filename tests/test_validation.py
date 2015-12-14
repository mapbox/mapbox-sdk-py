import pytest

from mapbox import validation


def test_latlon():
    assert -179.0 == validation.lon(-179.0)
    assert -89.0 == validation.lat(-89.0)

def test_lon_invalid():
    with pytest.raises(validation.MapboxValidationError):
        validation.lat(-91.0)
    with pytest.raises(validation.MapboxValidationError):
        validation.lon(-181.0)
