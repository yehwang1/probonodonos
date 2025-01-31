"""
probonodonos explore view.

URLs include:
/explore/
"""
import flask
import probonodonos

from probonodonos.views.helpers import check_ssesion, follow


@probonodonos.app.route('/explore/', methods=["GET", "POST"])
def show_explore():
    """Display /explore/ route."""
    logname, redirect = check_ssesion()
    if not logname:
        return redirect

    # Connect to database
    connection = probonodonos.model.get_db()

    if flask.request.method == "POST":
        username = flask.request.form['username']
        follow(connection, username, logname)

    cur = connection.execute(
        "SELECT username, "
        "filename FROM users "
        "WHERE username NOT IN "
        "(SELECT username2 "
        "FROM following "
        "WHERE username1 = ?) "
        "AND username != ?;", (logname, logname))

    not_following = cur.fetchall()

    for person in not_following:
        person["user_img_url"] = "/uploads/" + person.pop("filename")

    # Add database info to context
    context = {"logname": logname, "not_following": not_following}

    return flask.render_template(
        "explore.html", **context
    )  # this equals to flask.render_template("index.html", users = users)
