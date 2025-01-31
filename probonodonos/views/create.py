"""
probonodonos create view.

URLs include:
/accounts/create/
"""
import flask
import probonodonos

from probonodonos.views.helpers import create_new_password, upload_file


@probonodonos.app.route('/accounts/create/', methods=['GET', 'POST'])
def create():
    """Create an account."""
    if "user" in flask.session:
        return flask.redirect(flask.url_for("edit"))

    connection = probonodonos.model.get_db()

    if flask.request.method == 'POST':
        # inputs
        fullname = flask.request.form["fullname"]
        username = flask.request.form["username"]
        email = flask.request.form["email"]
        password = create_new_password(flask.request.form["password"])

        if_exists = connection.execute(
            "SELECT * FROM users WHERE username = ?;", (username, )
        ).fetchall()
        if len(if_exists) != 0:
            flask.abort(409)

        # upload the avatar
        fileobj = flask.request.files["file"]
        uuid_basename = upload_file(fileobj)

        connection.execute(
            "INSERT INTO users(username, fullname, email, filename, password) "
            "VALUES (?,?,?,?,?);",
            (username, fullname, email, uuid_basename, password))
        # log the user in
        flask.session["user"] = username
        return flask.redirect(flask.url_for("show_index"))

    return flask.render_template("create.html")
