```python

>>> from mapbox import Analytics
>>> analytics = Analytics()
>>> analytics._validate_resource_type('abc')
Traceback (most recent call last):
       	bla bla bla
ValueError: abc is not a valid profile
>>> analytics._validate_resource_type('accounts')
'accounts'
>>> analytics._validate_period(('a', 'b'))
Traceback (most recent call last):
       	bla bla bla
ValueError: Dates are not in ISO formatted string
>>> analytics._validate_period(('2016-03-22T00:00:00.000Z', '2016-03-19T00:00:00.000Z'))
Traceback (most recent call last):
       	bla bla bla
ValueError: The first date must be earlier than the second
>>> analytics._validate_period(('2015-03-22T00:00:00.000Z', '2016-03-22T00:00:00.000Z'))
Traceback (most recent call last):
       	bla bla bla
ValueError: The maximum period can be 1 year
>>> analytics._validate_period(('2015-03-20T00:00:00.000Z', '2015-03-29T00:00:00.000Z'))
('2015-03-20T00:00:00.000Z', '2015-03-29T00:00:00.000Z')
>>> response = analytics.analytics('accounts', 'amishas157', '', ('2016-03-22T00:00:00.000Z', '2016-03-24T00:00:00.000Z'), 'abc')
>>> response.status_code
401

```
