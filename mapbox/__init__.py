# mapbox
__version__ = "0.18.0"

from .services.analytics import Analytics
from .services.datasets import Datasets
from .services.directions import Directions
from .services.matrix import DirectionsMatrix
from .services.geocoding import (
    Geocoder, InvalidCountryCodeError, InvalidPlaceTypeError)
from .services.maps import Maps
from .services.mapmatching import MapMatcher
from .services.static import Static
from .services.static_style import StaticStyle
from .services.surface import Surface
from .services.tilequery import Tilequery
from .services.tilesets import Tilesets
from .services.uploads import Uploader
