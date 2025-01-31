"""
probonodonos delete view.

URLs include:
/accounts/delete/
"""
import flask
import probonodonos

from probonodonos.views.helpers import check_ssesion


@probonodonos.app.route('/accounts/delete/', methods=['GET', 'POST'])
def delete():
    """Delete the account."""
    connection = probonodonos.model.get_db()
    logname, redirect = check_ssesion()
    if not logname:
        if flask.request.method == "POST":
            flask.abort(403)
        else:
            return redirect

    if flask.request.method == 'POST':
        cur = connection.execute(
            "SELECT filename FROM users "
            "WHERE username = ?;", (logname, ))
        filename = cur.fetchall()[0]['filename']

        cur = connection.execute(
            "SELECT filename FROM posts "
            "WHERE owner = ?;", (logname, ))
        post_names = cur.fetchall()

        connection.execute("DELETE FROM users "
                           "WHERE username = ?;", (logname, ))
        detete_file_path = probonodonos.config.UPLOAD_FOLDER / filename
        detete_file_path.unlink()

        for name in post_names:
            postname = name["filename"]
            detete_file_path = probonodonos.config.UPLOAD_FOLDER / postname
            detete_file_path.unlink()

        flask.session.pop("user")  # delete session
        return flask.redirect(flask.url_for("create"))

    return flask.render_template("delete.html", logname=logname)
