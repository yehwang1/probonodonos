"""
Shared test fixtures.

Pytest will automatically run the client_setup_teardown() function before a
test.  A test should use "client" as an input, because the name of the fixture
is "client".

EXAMPLE:
>>> def test_simple(client):
>>>     response = client.get("/")
>>>     assert response.status_code == 200

Pytest docs:
https://docs.pytest.org/en/latest/fixture.html#conftest-py-sharing-fixture-functions

"""
import subprocess
import sqlite3
import pytest
import probonodonos


@pytest.fixture(name="client")
def client_setup_teardown():
    """
    Start a Flask test server with a clean database.

    Flask docs: https://flask.palletsprojects.com/en/1.1.x/testing/#testing
    """
    # Reset the database
    subprocess.run(["bin/probonodonosdb", "reset"], check=True)

    # Configure Flask test server
    probonodonos.app.config["TESTING"] = True

    # Transfer control to test.  The code before the "yield" statement is setup
    # code, which is executed before the test.  Code after the "yield" is
    # teardown code, which is executed at the end of the test.  Teardown code
    # is executed whether the test passed or failed.
    with probonodonos.app.test_client() as client:
        yield client


@pytest.fixture(name="db_connection")
def db_setup_teardown():
    """
    Create an in-memory sqlite3 database.

    This fixture is used only for the database tests, not the probonodonos tests.
    """
    # Create a temporary in-memory database
    db_connection = sqlite3.connect(":memory:")

    # Configure database to return dictionaries keyed on column name
    def dict_factory(cursor, row):
        """Convert database row objects to a dict keyed on column name."""
        return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
    db_connection.row_factory = dict_factory

    # Foreign keys have to be enabled per-connection.  This is an sqlite3
    # backwards compatibility thing.
    db_connection.execute("PRAGMA foreign_keys = ON")

    # Transfer control to test.  The code before the "yield" statement is setup
    # code, which is executed before the test.  Code after the "yield" is
    # teardown code, which is executed at the end of the test.  Teardown code
    # is executed whether the test passed or failed.
    yield db_connection

    # Verify foreign key support is still enabled
    cur = db_connection.execute("PRAGMA foreign_keys")
    foreign_keys_status = cur.fetchone()
    assert foreign_keys_status["foreign_keys"],\
        "Foreign keys appear to be disabled."

    # Destroy database
    db_connection.close()
