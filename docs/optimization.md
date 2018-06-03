# Optimization

The `Optimization` class provides access to the Mapbox Optimization API.  You can import it from either the `mapbox` module or the `mapbox.services.optimization` module.

__mapbox__:

```python
>>> from mapbox import Optimization

```

__mapbox.services.optimization__:

```python
>>> from mapbox.services.optimization import Optimization

```

See https://www.mapbox.com/api-documentation/#optimization for general documentation of the API.

Use of the Optimization API requires an access token, which you should set in your environment.  For more information, see the [access tokens](access_tokens.md) documentation.

## Optimization Method

The public method of the `Optimization` class provides access to the Optimization API and returns an instance of [`requests.Response`](http://docs.python-requests.org/en/latest/api/#requests.Response).


## Usage: Retrieving Optimizations

Instantiate `Optimization`.

```python
>>> optimization = Optimization()

```

Call the `route` method, passing in values for `features` and `profile`.  Pass in values for optional arguments as necessary - `geometries`, `overview`, `steps`, `waypoint_snapping`, `roundtrip`, `source`, `destination`, `distributions`, `annotations`, and `language`.

```python
>>> features = [
...    {
...        "type": "Feature",
...        "properties": {},
...        "geometry": 
...            {
...                "type": "Point",
...                "coordinates": 
...                    [
...                        0.0,
...                        0.0
...                    ]
...            }
...    }, 
...    {
...        "type": "Feature",
...        "properties": {},
...        "geometry": 
...            {
...                "type": "Point",
...                "coordinates": 
...                    [
...                        1.0,
...                        1.0
...                    ]
...            }
...    }
...]
>>> results = optimization.route(features, profile="mapbox/driving")

```

Evaluate whether the request succeeded, and retrieve the optimization object from the response object.

```python
>>> if results.status_code == 200:
...     optimization_object = response.json()
```
