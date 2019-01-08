# How to release

A source distribution (sdist) and wheels (bdist_wheel) for Python 2 and 3 are published to PyPI under the 'mapboxci' account
using [twine](https://twine.readthedocs.io/en/latest/index.html).

This process has been automated on Travis-CI. The 'mapboxci' account name and its token are stored on Travis-CI (see
`PYPI_USERNAME` and `PYPI_PASSWORD` in the project settings). Pushing a tag to GitHub will result in uploads to PyPI if the
build succeeds. You can make releases from the GitHub web page if you like.

Steps for making a release:

* Update the `__version__` attribute in mapbox/\_\_init\_\_.py. This project uses semantic versioning.
* Update the CHANGES file.
* Make a new tag that exactly matches the `__version__` attribute above.
* Push the tag and look for the new release and its binaries at https://pypi.org/project/mapbox/#history.
