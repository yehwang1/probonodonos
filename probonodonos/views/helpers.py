"""probonodonos view helper functions."""
import pathlib
import uuid
import hashlib
import flask
import probonodonos


def follow(connection, username, logname):
    """Add follow."""
    connection.execute(
        "INSERT INTO following(username1, username2) VALUES (?,?);",
        (logname, username))


def unfollow(connection, username, logname):
    """Unfollow."""
    connection.execute(
        "DELETE from following "
        "WHERE username1 = ? AND username2 = ?;", (logname, username))


def like(connection, postid, logname):
    """Like."""
    connection.execute("INSERT INTO likes(owner, postid) VALUES (?,?);",
                       (logname, postid))


def unlike(connection, postid, logname):
    """Unlike."""
    connection.execute("DELETE from likes "
                       "WHERE owner = ? AND postid = ?;", (logname, postid))


def comment(connection, postid, text, logname):
    """Comment."""
    connection.execute(
        "INSERT INTO comments(owner, postid, text) "
        "VALUES (?,?,?);", (logname, postid, text))


def uncomment(connection, commentid):
    """Uncomment."""
    connection.execute("DELETE from comments "
                       "WHERE commentid = ?;", (commentid, ))


def delete_post(connection, postid):
    """Delete_post."""
    cur = connection.execute("SELECT filename from posts "
                             "WHERE postid = ?;", (postid, ))
    filename = cur.fetchall()[0]['filename']

    connection.execute("DELETE from posts " "WHERE postid = ?;", (postid, ))
    return filename


def upload_file(fileobj):
    """Upload_file."""
    # Unpack flask object
    filename = fileobj.filename

    # Compute base name (filename without directory).  We use a UUID to avoid
    # clashes with existing files, and ensure that the name is compatible with
    # the filesystem.
    uuid_basename = "{stem}{suffix}".format(
        stem=uuid.uuid4().hex, suffix=pathlib.Path(filename).suffix)
    # Save to disk
    path = probonodonos.app.config["UPLOAD_FOLDER"] / uuid_basename
    fileobj.save(path)

    return uuid_basename


def create_post(fileobj, connection, username):
    """Create_post."""
    uuid_basename = upload_file(fileobj)

    connection.execute("INSERT INTO posts(filename, owner) "
                       "VALUES (?,?);", (uuid_basename, username))


def checkpassword(connection, password, username):
    """Checkpassword."""
    # Make sure that you are using the salt stored in the database
    # Randomly generating a salt using the uuid library when creating
    # a new user.

    # 1. Read password entry from database: sha512$<SALT>$<HASHED_PASSWORD>
    content = connection.execute(
        "SELECT password FROM users "
        "WHERE username = ?;", (username, )).fetchall()

    if len(content) != 1:  # no such user in db
        flask.abort(403)
    password_db_string = content[0]["password"]
    algorithm, salt, password_hash = password_db_string.split('$')

    # 2. Compute sha512(<SALT> + input_password)
    credential = encrypt(password, salt, algorithm)

    # 3. Check if it matches <HASHED_PASSWORD>
    if credential != password_hash:
        print("bad")
        flask.abort(403)
    else:
        print("success")
    return credential == password_hash


# Return: hashed(salt+password)
def encrypt(password, salt, algorithm='sha512'):
    """Encrypt."""
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    return password_hash


# Return: algorithm$<SALT>$hashed(salt+password)
def create_new_password(password):
    """Create_new_password."""
    if not password:
        flask.abort(400)
    # a new salt
    salt = uuid.uuid4().hex
    algorithm = 'sha512'
    password_hash = encrypt(password, salt, algorithm)
    password_db_string = "$".join([algorithm, salt, password_hash])
    print(password_db_string)
    return password_db_string


def switch_follow(connection, logname):
    """Follow button."""
    if flask.request.method == "POST":
        dicts = flask.request.form
        user = dicts["username"]
        if "follow" in dicts.keys():
            follow(connection, user, logname)
        elif "unfollow" in dicts.keys():
            unfollow(connection, user, logname)


def check_ssesion():
    """Check if login person's information in ssesion."""
    logname, redirect = None, None
    if "user" in flask.session:
        logname = flask.session["user"]
    else:
        redirect = flask.redirect(flask.url_for("login"))
    return logname, redirect


def check_user(connection, user_url_slug):
    """Check if user_url_slug does not exist in the database."""
    check = connection.execute(
        "SELECT * FROM users WHERE username = ?;", (user_url_slug, )
    ).fetchall()
    if len(check) == 0:
        flask.abort(404)
