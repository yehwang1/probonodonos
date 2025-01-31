"""
Test student-created utility scripts.




"""
import os
import subprocess
import sqlite3


def test_executables():
    """Verify probonodonosrun, probonodonostest, probonodonosdb are executables."""
    assert_is_shell_script("bin/probonodonosrun")
    assert_is_shell_script("bin/probonodonostest")
    assert_is_shell_script("bin/probonodonosdb")


def test_probonodonosdb_destroy():
    """Verify probonodonosdb destroy removes DB file."""
    subprocess.run(["bin/probonodonosdb", "destroy"], check=True)
    assert not os.path.exists("var/probonodonos.sqlite3")
    assert not os.path.exists("var/uploads")


def test_probonodonosdb_create():
    """Verify probonodonosdb create populates DB with default data."""
    # Destroy, then create database
    subprocess.run(["bin/probonodonosdb", "destroy"], check=True)
    subprocess.run(["bin/probonodonosdb", "create"], check=True)

    # Verify files were created
    assert os.path.exists("var/probonodonos.sqlite3")
    assert os.path.exists(
        "var/uploads/5ecde7677b83304132cb2871516ea50032ff7a4f.jpg")
    assert os.path.exists(
        "var/uploads/73ab33bd357c3fd42292487b825880958c595655.jpg")
    assert os.path.exists(
        "var/uploads/122a7d27ca1d7420a1072f695d9290fad4501a41.jpg")
    assert os.path.exists(
        "var/uploads/ad7790405c539894d25ab8dcf0b79eed3341e109.jpg")
    assert os.path.exists(
        "var/uploads/505083b8b56c97429a728b68f31b0b2a089e5113.jpg")
    assert os.path.exists(
        "var/uploads/9887e06812ef434d291e4936417d125cd594b38a.jpg")
    assert os.path.exists(
        "var/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg")
    assert os.path.exists(
        "var/uploads/2ec7cf8ae158b3b1f40065abfb33e81143707842.jpg")

    # Connect to the database
    connection = sqlite3.connect("var/probonodonos.sqlite3")
    connection.execute("PRAGMA foreign_keys = ON")

    # There should be 4 rows in the 'users' table
    cur = connection.execute("SELECT count(*) FROM users")
    num_rows = cur.fetchone()[0]
    assert num_rows == 4


def test_probonodonosdb_reset():
    """Verify probonodonosdb reset does a destroy and a create."""
    # Create a "stale" database file
    with open("var/probonodonos.sqlite3", "w") as outfile:
        outfile.write("this should be overwritten")

    # Reset the database
    subprocess.run(["bin/probonodonosdb", "reset"], check=True)

    # Verify database file was overwritten.  Note that we have to open the file
    # in binary mode because sqlite3 format is not plain text.
    with open("var/probonodonos.sqlite3", "rb") as infile:
        content = infile.read()
    assert b"this should be overwritten" not in content


def test_probonodonosdb_dump():
    """Spot check probonodonosdb dump for a few data points."""
    subprocess.run(["bin/probonodonosdb", "reset"], check=True)
    output = subprocess.run(
        ["bin/probonodonosdb", "dump"],
        check=True, stdout=subprocess.PIPE, universal_newlines=True,
    ).stdout
    assert "awdeorio" in output
    assert "73ab33bd357c3fd42292487b825880958c595655.jpg" in output
    assert "Walking the plank" in output


def assert_is_shell_script(path):
    """Assert path is an executable shell script."""
    assert os.path.isfile(path)
    output = subprocess.run(
        ["file", path],
        check=True, stdout=subprocess.PIPE, universal_newlines=True,
    ).stdout
    assert "shell script" in output
    assert "executable" in output
