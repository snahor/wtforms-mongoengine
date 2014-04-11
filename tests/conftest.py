import pytest
from mongoengine import connect

DB_NAME = 'wtforms_mongoengine_test'


@pytest.fixture(scope='function')
def conn(request):
    conn = connect(DB_NAME)

    def teardown():
        conn.drop_database(DB_NAME)

    request.addfinalizer(teardown)
    return conn
