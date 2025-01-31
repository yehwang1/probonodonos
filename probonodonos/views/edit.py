"""
probonodonos edit view.

URLs include:
/accounts/edit/
"""
import flask
import probonodonos

from probonodonos.views.helpers import upload_file, check_ssesion


@probonodonos.app.route('/accounts/edit/', methods=['GET', 'POST'])
def edit():
    """Edit the account profile."""
    logname, redirect = check_ssesion()
    if not logname:
        return redirect

    connection = probonodonos.model.get_db()

    if flask.request.method == 'POST':
        fileobj = flask.request.files["file"]
        filename = fileobj.filename
        if filename != '':
            cur = connection.execute(
                "SELECT filename FROM users "
                "WHERE username = ?;", (logname, ))
            filename = cur.fetchall()[0]['filename']
            detete_file_path = probonodonos.config.UPLOAD_FOLDER / filename
            detete_file_path.unlink()

            uuid_basename = upload_file(fileobj)
            connection.execute(
                "UPDATE users "
                "SET filename = ? "
                "WHERE username = ?;", (uuid_basename, logname))

        fullname = flask.request.form["fullname"]
        email = flask.request.form["email"]
        connection.execute(
            "UPDATE users "
            "SET fullname = ?, email = ? "
            "WHERE username = ?;", (fullname, email, logname))

    owner = connection.execute(
        "SELECT filename, fullname, email FROM users WHERE username = ?;",
        (logname, )).fetchall()
    src = "/uploads/" + owner[0]["filename"]
    prev_fullname = owner[0]["fullname"]
    prev_email = owner[0]["email"]

    return flask.render_template("edit.html",
                                 logname=logname,
                                 avatar_src=src,
                                 email=prev_email,
                                 fullname=prev_fullname)
