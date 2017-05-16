# Analytics

The `Analytics` class from the `mapbox.services.analytics` module provides
access to the Mapbox Analytics API. You can also import it directly from the
`mapbox` module. 

**Note**: This API is available only for premium and enterprise plans.

```python
>>> from mapbox import Analytics

```


See https://www.mapbox.com/api-documentation/#analytics for general documentation of the API.

Your Mapbox access token should be set in your environment; see the [access
tokens](access_tokens.md) documentation for more information.

## Analytics methods

The methods of `Analytics` class that provide access to the Analytics API return an instance of 
[`requests.Response`](http://docs.python-requests.org/en/latest/api/#requests.Response). `Analytics` response also include the `json()` method which returns Python data parsed from API.

## Usage

The Mapbox Analytics API is used to get API usage for services by resource. It returns counts per day for given resource and period.

```python
>>> analytics = Analytics()

```

The input to `analytics` method are resource_type, username, id, period, access_token.

```python
>>> response = analytics.analytics('accounts', 'mapbox-sdk-py-user')
>>> response.status_code
200

```
