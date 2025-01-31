"""
probonodonos following view.

URLs include:
/u/<user_url_slug>/following/
"""
import flask
import probonodonos

from probonodonos.views.helpers import switch_follow, check_ssesion, check_user


@probonodonos.app.route('/u/<user_url_slug>/following/', methods=["GET", "POST"])
def show_following(user_url_slug):
    """Display /u/<user_url_slug>/following/ route."""
    logname, redirect = check_ssesion()
    if not logname:
        return redirect

    # Connect to database
    connection = probonodonos.model.get_db()
    check_user(connection, user_url_slug)

    # under <user_url_slug> page
    username = user_url_slug

    switch_follow(connection, logname)

    followings = connection.execute(
        "SELECT username, filename "
        "FROM users "
        "WHERE username IN "
        "(SELECT username2 "
        "FROM following "
        "WHERE username1 = ?) "
        "ORDER BY username ASC;", (username, )).fetchall()

    for following in followings:
        # key: owner_img_url
        following["user_img_url"] = "/uploads/" + following.pop("filename")

        # key: logname_follows_username
        following_list = connection.execute(
            "SELECT username2 "
            "FROM following "
            "WHERE username1 = ?;", (logname, )).fetchall()
        following["logname_follows_username"] = ({
            'username2':
            following["username"]
        } in following_list)

    # Add database info to context
    context = {"logname": logname, "following": followings, "user": username}
    return flask.render_template("following.html", **context)
