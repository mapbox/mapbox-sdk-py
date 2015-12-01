README
======

Module docs in this folder are written as Python doctests embedded in Markdown.

To run the doctests from this directory against the Mapbox API using your own
Mapbox API access token, do the following.

```bash
MAPBOX_ACCESS_TOKEN="MY_ACCESS_TOKEN" py.test --doctest-glob='*.md' *.md
```

See this project's `.travis.yml` file for more doctest usage.
