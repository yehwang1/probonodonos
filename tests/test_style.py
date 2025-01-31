"""
Check Python style with pycodestyle, pydocstyle and pylint.




"""
import os
import pathlib
import shutil
import collections
from urllib.parse import urlparse
import subprocess
import bs4
import utils


def test_pycodestyle():
    """Run pycodestyle."""
    assert_no_prohibited_terms("nopep8", "noqa", "pylint")
    subprocess.run(["pycodestyle", "setup.py", "probonodonos"], check=True)


def test_pydocstyle():
    """Run pydocstyle."""
    assert_no_prohibited_terms("nopep8", "noqa", "pylint")
    subprocess.run(["pydocstyle", "setup.py", "probonodonos"], check=True)


def test_pylint():
    """Run pylint."""
    assert_no_prohibited_terms("nopep8", "noqa", "pylint")
    subprocess.run([
        "pylint",
        "--rcfile", utils.TEST_DIR/"testdata/pylintrc",
        "--disable=cyclic-import",
        "setup.py",
        "probonodonos",
    ], check=True)


def test_html(client):
    """Validate generated HTML5 in probonodonos/templates/ ."""
    # Log in as awdeorio
    response = client.post(
        "/accounts/login/",
        data={"username": "awdeorio", "password": "password"},
    )
    assert response.status_code == 302

    # Clean up
    if os.path.exists("tmp/localhost"):
        shutil.rmtree("tmp/localhost")

    # Render all pages and download HTML to ./tmp/localhost/
    crawl(
        client=client,
        outputdir="tmp/localhost",
        todo=collections.deque(["/"]),
        done=set(),
    )

    # Verify downloaded pages HTML5 compliances using html5validator
    print("html5validator --root tmp/localhost")
    subprocess.run([
        "html5validator",
        "--root", "tmp/localhost",
        "--ignore", "JAVA_TOOL_OPTIONS",
    ], check=True)


def assert_no_prohibited_terms(*terms):
    """Check for prohibited terms before testing style."""
    for term in terms:
        completed_process = subprocess.run(
            [
                "grep",
                "-r",
                "-n",
                term,
                "--include=*.py",
                "--include=*.jsx",
                "--include=*.js",
                "--exclude=__init__.py",
                "--exclude=setup.py",
                "--exclude=bundle.js",
                "--exclude=*node_modules/*",
                "probonodonos",
            ],
            check=False,  # We'll check the return code manually
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )

        # Grep exit code should be non-zero, indicating that the prohibited
        # term was not found.  If the exit code is zero, crash and print a
        # helpful error message with a filename and line number.
        assert completed_process.returncode != 0, (
            "The term '{term}' is prohibited.\n{message}"
            .format(term=term, message=completed_process.stdout)
        )


def crawl(client, outputdir, todo, done):
    """Recursively render every page provided by 'client', saving to file."""
    if not todo:
        return

    # Pop a URL off the head of the queue and parse it
    url = todo.popleft()
    hostname = urlparse(url).hostname
    path = urlparse(url).path

    # Ignore links outside localhost
    if hostname and hostname not in ["localhost", "127.0.01"]:
        done.add(path)
        crawl(client, outputdir, todo, done)
        return

    # Ignore links already visited
    if path in done:
        done.add(path)
        crawl(client, outputdir, todo, done)
        return

    # Ignore logout route
    if "logout" in path:
        done.add(path)
        crawl(client, outputdir, todo, done)
        return

    # Download
    print("GET", path)
    response = client.get(path)
    assert response.status_code == 200

    # Save
    assert path.endswith("/"),\
        "Error: path does not end in slash: '{}'".format(path)
    outputdir = pathlib.Path(outputdir)
    dirname = outputdir/"localhost"/path.lstrip("/")
    dirname.mkdir(parents=True, exist_ok=True)
    filename = dirname/"index.html"
    html = response.data.decode(response.charset)
    with filename.open("w") as outfile:
        outfile.write(html)

    # Update visited list
    done.add(path)

    # Extract links and add to todo list
    soup = bs4.BeautifulSoup(html, "html.parser")
    for link_elt in soup.find_all("a"):
        link = link_elt.get("href")
        if link in done:
            continue
        todo.append(link)

    # Recurse
    crawl(client, outputdir, todo, done)
