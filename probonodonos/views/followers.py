"""
probonodonos followers view.

URLs include:
/u/<user_url_slug>/followers/
"""
import flask
import probonodonos

from probonodonos.views.helpers import switch_follow, check_ssesion, check_user


@probonodonos.app.route('/u/<user_url_slug>/followers/', methods=["GET", "POST"])
def show_followers(user_url_slug):
    """Display /u/<user_url_slug>/followers/ route."""
    # Connect to database
    connection = probonodonos.model.get_db()
    logname, redirect = check_ssesion()
    if not logname:
        return redirect

    check_user(connection, user_url_slug)

    # under <user_url_slug> page
    username = user_url_slug

    switch_follow(connection, logname)

    followers = connection.execute(
        "SELECT username, filename "
        "FROM users "
        "WHERE username IN "
        "(SELECT username1 "
        "FROM following "
        "WHERE username2 = ?) "
        "ORDER BY username ASC;", (username, )).fetchall()

    for follower in followers:
        # key: owner_img_url
        follower["user_img_url"] = "/uploads/" + follower.pop("filename")

        # key: logname_follows_username
        follower_list = connection.execute(
            "SELECT username2 "
            "FROM following "
            "WHERE username1 = ?;", (logname, )).fetchall()
        follower["logname_follows_username"] = ({
            'username2':
            follower["username"]
        } in follower_list)

    # Add database info to context
    context = {"logname": logname, "followers": followers, "user": username}
    return flask.render_template("followers.html", **context)
