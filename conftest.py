import os

import pytest


@pytest.fixture
def uploads_dest_id():
    return 'uploads-{0}'.format(
        os.environ.get('TRAVIS_PYTHON_VERSION', 'test'))
