from codecs import open as codecs_open

from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

# Parse the version from the mapbox module.
with open('mapbox/__init__.py') as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            continue

setup(name='mapbox',
      version=version,
      description="A Python client for Mapbox services",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author="Sean Gillies",
      author_email='sean@mapbox.com',
      url='https://github.com/mapbox/mapbox-sdk-py',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'click',
          'click-plugins',
          'cligj',
          'requests',
          'uritemplate.py',
          'boto3',
      ],
      extras_require={
          'test': [
              'coveralls', 'pytest>=2.8.3', 'pytest-cov', 'responses', 'tox']})
