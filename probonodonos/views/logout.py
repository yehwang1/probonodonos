"""
probonodonos logout view.

URLs include:
/accounts/logout/
"""
import flask
import probonodonos


@probonodonos.app.route('/accounts/logout/', methods=['POST'])
def logout():
    """Logout."""
    # should only accept POST requests
    flask.session.pop("user")
    return flask.redirect(flask.url_for("login"))
