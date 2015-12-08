import os

import pytest


@pytest.fixture
def uploads_dest_id():
    version = os.environ.get('TRAVIS_PYTHON_VERSION', 'test')
    return 'uploads-{0}'.format(version.replace(".", "-"))
