# Tokens

The `Tokens` class (`from mapbox import Tokens`) provides
access to the Mapbox Tokens API, allowing you to programmaticaly create
Mapbox access tokens to access Mapbox resources on behalf of a user.

```python

>>> from mapbox import Tokens
>>> service = Tokens()

```

See https://www.mapbox.com/api-documentation/#tokens for general documentation of the API.

This API requires an **initial token** with the `tokens:write` scope.
Your Mapbox access token should be set in your environment;
see the [access tokens](access_tokens.md) documentation for more information.

The Mapbox username associated with each account is determined by the access_token by default. All of the methods also take an optional `username` keyword argument to override this default.

## List tokens

```python

>>> response = service.list_tokens()
>>> response.json()
[...]

```

## Create temporary tokens

Generate a token for temporary access to mapbox APIs using the 
`create_temp_token` method.  Tokens can bet set to expire at any time up to one hour.

```python

>>> response = service.create_temp_token(
...     scopes=['styles:read'],
...     expires=60)  # seconds
>>> auth = response.json()
>>> auth['token'][:3]
'tk.'

```


## Create a permanet token


```python

>>> response = service.create(
...     scopes=['styles:read'],
...     note='test-token')
>>> auth = response.json()
>>> auth['scopes']
['styles:read']
>>> auth['token'][:3]
'pk.'

```

If you create a token with public/read scopes, your token with be a public token, starting with `pk`. If the token has secret/write scopes, the token will be secret, starting with `sk`.

If you want to create a token that may contain secret/write scopes, you must create the token with at least one such scope initially.

## Update a token

To update the scopes of a token

```python

>>> response = service.update(
...     authorization_id=auth['id'],
...     scopes=['styles:read', 'datasets:read'],
...     note="updated")
>>> auth = response.json()
>>> assert response.status_code == 200


```

## Check validity of a token

```python

>>> service.check_validity().json()['code']
'TokenValid'

```

Note that this applies only to the access token which is making the request.
If you want to check the validity of other tokens, you must make a separate instance of the `Tokens` service class using the desired `access_token`.

```python

>>> new_service = Tokens(access_token=auth['token'])

```

## List the scopes of a token

```python

>>> response = service.list_scopes()
>>> response.json()
[...]

```

As with checking validity, this method applies only to the access token which is making the request.


## Delete a token

```python

>>> response = service.delete(
...     authorization_id=auth['id'])
>>> assert response.status_code == 204

```


