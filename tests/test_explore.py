"""
Test /u/explore/ URL.


"""
import re
import bs4


def test_awdeorio_default(client):
    """Verify default content at /explore/ with awdeorio logged in."""
    # Login
    response = client.post(
        "/accounts/login/",
        data={"username": "awdeorio", "password": "password"},
    )
    assert response.status_code == 302

    # Load and parse explore page
    response = client.get("/explore/")
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.data, "html.parser")
    srcs = [x.get("src") for x in soup.find_all('img')]
    links = [x.get("href") for x in soup.find_all("a")]
    buttons = [submit.get("name") for button in soup.find_all('form')
               for submit in button.find_all("input") if submit]

    # Verify links in header
    assert "/" in links
    assert "/explore/" in links
    assert "/u/awdeorio/" in links

    # Verify links specific to /explore/
    assert "/u/jag/" in links
    assert "/u/jflinn/" not in links
    assert "/u/michjc/" not in links

    # Verify images
    assert "/uploads/73ab33bd357c3fd42292487b825880958c595655.jpg" in srcs
    assert "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg" not in srcs
    assert "/uploads/505083b8b56c97429a728b68f31b0b2a089e5113.jpg" not in srcs
    assert "/uploads/5ecde7677b83304132cb2871516ea50032ff7a4f.jpg" not in srcs

    # Verify buttons
    assert "follow" in buttons
    assert "username" in buttons
    assert "unfollow" not in buttons
    assert "commentid" not in buttons
    assert "postid" not in buttons
    assert "delete" not in buttons


def test_follow(client):
    """Click follow, then check /u/<user_url_slug>/following/ ."""
    # Login
    response = client.post(
        "/accounts/login/",
        data={"username": "awdeorio", "password": "password"},
    )
    assert response.status_code == 302

    # Follow jag
    response = client.post(
        "/explore/",
        data={"follow": "follow", "username": "jag"},
    )
    assert response.status_code == 200

    # Load and parse following page
    response = client.get("/u/awdeorio/following/")
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.data, "html.parser")
    text = soup.get_text()
    text = re.sub(r"\s+", " ", text)
    srcs = [x.get("src") for x in soup.find_all('img')]
    links = [x.get("href") for x in soup.find_all("a")]

    # Verify links in header are present
    assert "/" in links
    assert "/explore/" in links
    assert "/u/awdeorio/" in links

    # Verify text
    # Check for following 3 people + the header "following" at the top
    assert text.lower().count("following") == 4
    assert "not following" not in text.lower()

    # Verify images: Mike, Jason, Jag
    assert "/uploads/5ecde7677b83304132cb2871516ea50032ff7a4f.jpg" in srcs
    assert "/uploads/505083b8b56c97429a728b68f31b0b2a089e5113.jpg" in srcs
    assert "/uploads/73ab33bd357c3fd42292487b825880958c595655.jpg" in srcs

    # Verify links
    assert "/u/jflinn/" in links
    assert "/u/michjc/" in links
    assert "/u/jag/" in links


def test_empty(client):
    """Nobody shows up when you're following everyone."""
    # Login
    response = client.post(
        "/accounts/login/",
        data={"username": "awdeorio", "password": "password"},
    )
    assert response.status_code == 302

    # Follow jag
    response = client.post(
        "/explore/",
        data={"follow": "follow", "username": "jag"},
    )
    assert response.status_code == 200

    # Load and parse explore page
    response = client.get("/explore/")
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.data, "html.parser")
    text = soup.get_text()
    text = re.sub(r"\s+", " ", text)
    srcs = [x.get("src") for x in soup.find_all('img')]
    links = [x.get("href") for x in soup.find_all("a")]
    buttons = [submit.get("name") for button in soup.find_all('form')
               for submit in button.find_all("input") if submit]

    # Verify links in header
    assert "/" in links
    assert "/explore/" in links
    assert "/u/awdeorio/" in links

    # Verify links specific to /explore/
    assert "/u/jag/" not in links
    assert "/u/jflinn/" not in links
    assert "/u/michjc/" not in links

    # Verify images: nobody shows up
    assert "/uploads/73ab33bd357c3fd42292487b825880958c595655.jpg" not in srcs
    assert "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg" not in srcs
    assert "/uploads/505083b8b56c97429a728b68f31b0b2a089e5113.jpg" not in srcs
    assert "/uploads/5ecde7677b83304132cb2871516ea50032ff7a4f.jpg" not in srcs

    # Verify buttons
    assert "follow" not in buttons
    assert "username" not in buttons
    assert "unfollow" not in buttons
    assert "commentid" not in buttons
    assert "postid" not in buttons
    assert "delete" not in buttons
