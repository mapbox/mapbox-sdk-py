# Styles

The `Styles` class provides access to the Mapbox Styles API.  You can import it from either the `mapbox` module or the `mapbox.services.styles` module.

__mapbox__:

```python
>>> from mapbox import Styles

```

__mapbox.services.styles__:

```python
>>> from mapbox.services.styles import Styles

```

See https://www.mapbox.com/api-documentation/#styles for general documentation of the API.

Use of the Styles API requires an access token, which you should set in your environment.  For more information, see the [access tokens](access_tokens.md) documentation.

## Styles Methods

The public methods of the `Styles` class provide access to the Styles API and return an instance of [`requests.Response`](http://docs.python-requests.org/en/latest/api/#requests.Response).

## Usage: Retrieving a Style

Instantiate `Styles`.

```python
>>> styles = Styles()

```

Call the `style` method, passing in a value for `style_id`.

```python
>>> response = styles.style("mapbox://styles/mapbox/streets-v10")

```

Evaluate whether the request succeeded, and retrieve the style object.

```python
>>> if response.status_code == 200:
...     style_object = response.json()

```

## Usage: Listing Styles

Instantiate `Styles`.

```python
>>> styles = Styles()

```

Call the `list_styles` method.

```python
>>> response = styles.list_styles()

```

Evaluate whether the request succeeded, and retrieve the style metadata.

```python
>>> if response.status_code == 200:
...     metadata = response.json()

```

## Usage: Creating a Style

Instantiate `Styles`.

```python
>>> styles = Styles()

```

Call the `create_style` method, passing in a value for `style_object`.  `style_object` may be a dict or a file.


__dict__:

```python
>>> response = styles.create_style({"key": "value"})

```

__file__:

```python
>>> response = styles.create_style("./style_object.json")

```

Evaluate whether the request succeeded, and retrieve the properties of the style object.

```python
>>> if response.status_code == 200:
...     properties = response.json()

```

Validation of `style_object` occurs on the server.  Invalid styles wil produce a descriptive validation error.

## Usage: Updating a Style

Instantiate `Styles`.

```python
>>> styles = Styles()

```

Call the `update_style` method, passing in a value for `style_object`.  `style_object` may be a dict or a file.


__dict__:

```python
>>> response = styles.update_style({"key": "value"})

```

__file__:

```python
>>> response = styles.update_style("./style_object.json")

```

Evaluate whether the request succeeded, and retrieve the properties of the style object.

```python
>>> if response.status_code == 200:
...     properties = response.json()

```

Most validation of `style_object` occurs on the server.  Local validation is trivial, involving only the removal of the "created" and "modified" keys from `style_object`.  Invalid styles wil produce a descriptive validation error.

## Usage: Deleting a Style

Instantiate `Styles`.

```python
>>> styles = Styles()

```

Call the `delete_style` method, passing in a value for `style_id`.

```python
>>> response = styles.style("mapbox://styles/mapbox/streets-v10")

```

Evaluate whether the request succeeded.

```python
>>> if response.status_code == 204:
...     print("success")

```

## Usage: Retrieving a Font Glyph Range

Instantiate `Styles`.

```python
>>> styles = Styles()

```

Call the `font_glyphs` method, passing in values for `fonts` and `start`.

```python
>>> response = styles.font_glyphs(["first-font, "second-font"], 256)

```

Evaluate whether the request succeeded, and retrieve the font glyph range.  (The font glyphs will be encoded as a protocol buffer, the decoding of which falls outside of the scope of this document.)

```python
>>> if response.status_code == 200\
...     and "application/x-protobuf" in response.headers:
...         font_glyphs = response.content
```

## Usage: Retrieving a Sprite Image or JSON

Instantiate `Styles`.

```python
>>> styles = Styles()

```

Call the `get_sprite` method, passing in values for `style_id` and `sprite`.  Pass in values for optional arguments as necessary - `retina` (double scale) and `file_format`.


```python
>>> response = styles.get_sprite("mapbox://styles/mapbox/streets-v10", "sprite")

```

Evaluate whether the request succeeded, and retrieve the sprite image or JSON from the response object.  The approach will depend upon the file format.

__image__:

```python
>>> if response.status_code == 200:
...     with open("./sprite", "wb") as output:
...         output.write(response.content)

```

__JSON__:
```python
>>> if response.status_code == 200:
...     sprite = response.json()

```

## Usage: Adding a New Image to a Sprite

Instantiate `Styles`.

```python
>>> styles = Styles()

```

Call the `add_image` method, passing in values for `style_id`, `sprite`, and `icon_name`.

```python
>>> response = styles.add_image("mapbox://styles/mapbox/streets-v10", "sprite", "icon.svg")

```

Evaluate whether the request succeeded, and retrieve the properties of the added image.

```python
>>> if response.status_code == 200:
...     properties = response.json()

```

## Usage: Deleting an Existing Image from a Sprite

Instantiate `Styles`.

```python
>>> styles = Styles()

```

Call the `delete_image` method, passing in values for `style_id`, `sprite`, and `icon_name`.

```python
>>> response = styles.delete_image("mapbox://styles/mapbox/streets-v10", "sprite", "icon.svg")

```

Evaluate whether the request succeeded, and retrieve the properties of the deleted image.

```python
>>> if response.status_code == 200:
...     properties = response.json()

```
