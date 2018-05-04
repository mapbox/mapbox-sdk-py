from codecs import open as codecs_open

from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

# Parse the version from the mapbox module.
with open('mapbox/__init__.py') as f:
    for line in f:
        if "__version__" in line:
            version = line.split("=")[1].strip().strip('"').strip("'")
            continue

setup(name='mapbox',
      version=version,
      description="A Python client for Mapbox services",
      long_description=long_description,
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6'],
      keywords='',
      author="Sean Gillies",
      author_email='sean@mapbox.com',
      url='https://github.com/mapbox/mapbox-sdk-py',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'boto3>=1.4',
          'cachecontrol',
          'iso3166',
          'python-dateutil>=2.5.0'
          'requests',
          'polyline>=1.3.1',
          'uritemplate>=2.0'],
      extras_require={
          'test': [
              'coveralls', 'pytest>=2.8.3', 'pytest-cov', 'responses', 'tox']})
