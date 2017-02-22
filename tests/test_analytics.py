import mapbox
import pytest

def test_profile_invalid():
    """'jetpack' is not a valid profile."""
    with pytest.raises(ValueError):
        mapbox.Analytics(access_token='pk.test')._validate_resource_type('jetpack')
