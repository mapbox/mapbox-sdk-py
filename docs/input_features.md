# Input features

Many of the Mapbox APIs take geographic features (waypoints) as input.

The `mapbox` module supports the following inputs

* An iterable of GeoJSON-like `Feature`s
* An iterable of objects which implement the [`__geo_interface__`](https://gist.github.com/sgillies/2217756)
