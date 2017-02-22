```python

>>> from mapbox import Analytics
>>> analytics = Analytics()
>>> analytics._validate_resource_type('abc')
Traceback (most recent call last):
       	bla bla bla
ValueError: abc is not a valid profile
>>> analytics._validate_resource_type('accounts')
'accounts'

```
