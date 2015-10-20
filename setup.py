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
          'click', 'click-plugins', 'cligj', 'requests', 'uritemplate.py'
      ],
      extras_require={
          'test': ['coveralls', 'pytest', 'pytest-cov', 'responses'],
      },
      entry_points="""
      [console_scripts]
      mbx=mapbox.scripts.cli:main_group

      [mapbox.mapbox_commands]
      geocode=mapbox.scripts.geocoder:geocode
      create_dataset=mapbox.scripts.datasets:create_dataset
      ls_datasets=mapbox.scripts.datasets:ls_datasets
      retrieve_features=mapbox.scripts.datasets:retrieve_features
      update_features=mapbox.scripts.datasets:update_features
      """
      )
