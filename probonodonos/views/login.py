"""
probonodonos login view.

URLs include:
/accounts/login/
"""
import flask
import probonodonos

from probonodonos.views.helpers import checkpassword


@probonodonos.app.route('/accounts/login/', methods=['GET', 'POST'])
def login():
    """Login."""
    connection = probonodonos.model.get_db()

    if flask.request.method == 'POST':
        username = flask.request.form["username"]
        password = flask.request.form["password"]

        if checkpassword(connection, password, username):
            # start session
            flask.session["user"] = username
            # If logged in, redirect to /.
            return flask.redirect(flask.url_for("show_index"))

    return flask.render_template("login.html")
