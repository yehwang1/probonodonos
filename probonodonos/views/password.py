"""
probonodonos password view.

URLs include:
/accounts/password/
"""
import flask
import probonodonos

from probonodonos.views.helpers import checkpassword, create_new_password


@probonodonos.app.route('/accounts/password/', methods=['GET', 'POST'])
def password():
    """Password."""
    if "user" in flask.session:
        logname = flask.session["user"]
    else:
        return flask.redirect(flask.url_for("login"))

    connection = probonodonos.model.get_db()

    if flask.request.method == 'POST':
        # inputs
        pass_word = flask.request.form["password"]
        new_password1 = flask.request.form["new_password1"]
        new_password2 = flask.request.form["new_password2"]

        # Check the user’s password and abort(403) if it fails.
        if checkpassword(connection, pass_word, logname):

            # Check if both new passwords match. abort(401) otherwise.
            if new_password1 != new_password2:
                flask.abort(401)

            new_password = create_new_password(new_password1)
            connection.execute(
                "UPDATE users "
                "SET password = ? "
                "WHERE username = ?;", (new_password, logname))

            return flask.redirect(flask.url_for("edit"))

    return flask.render_template("password.html", logname=logname)
