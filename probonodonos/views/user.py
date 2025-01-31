"""
probonodonos user view.

URLs include:
/u/<user_url_slug>/
"""
import flask
import probonodonos

from probonodonos.views.helpers import (follow, unfollow, create_post,
                                    check_ssesion, check_user)


@probonodonos.app.route('/u/<user_url_slug>/', methods=["GET", "POST"])
def show_user(user_url_slug):
    """Display /u/<user_url_slug>/ route."""
    logname, redirect = check_ssesion()
    if redirect:
        return redirect

    # Connect to database
    connection = probonodonos.model.get_db()
    check_user(connection, user_url_slug)

    if flask.request.method == "POST":
        dicts = flask.request.form
        if "follow" in dicts.keys():
            user = dicts["username"]
            follow(connection, user, logname)
        elif "unfollow" in dicts.keys():
            user = dicts["username"]
            unfollow(connection, user, logname)
        elif "create_post" in dicts.keys():
            fileobj = flask.request.files["file"]
            create_post(fileobj, connection, user_url_slug)

    # fullname
    fullname = connection.execute(
        "SELECT fullname FROM users "
        "WHERE username = ?;", (user_url_slug, )
    ).fetchall()[0]["fullname"]

    # if_follow
    following_list = connection.execute(
        "SELECT username2 FROM following WHERE username1 = ?;", (logname, )
    ).fetchall()
    if_follow = ({'username2': user_url_slug} in following_list)

    # flollowers
    followers = connection.execute(
        "SELECT COUNT(username1) "
        "FROM following "
        "WHERE username2 = ?;", (user_url_slug, )
    ).fetchall()[0]["COUNT(username1)"]

    # posts
    posts = connection.execute(
        "SELECT * FROM posts "
        "WHERE owner = ? "
        "ORDER BY postid ASC;", (user_url_slug, )).fetchall()
    for post in posts:
        post["img_url"] = "/uploads/" + post.pop("filename")
        post.pop("owner")
        post.pop("created")

    # Add database info to context
    context = {
        "logname": logname,
        "username": user_url_slug,
        "logname_follows_username": if_follow,
        "fullname": fullname,
        "following": len(following_list),
        "followers": followers,
        "total_posts": len(posts),
        "posts": posts
    }
    return flask.render_template("user.html", **context)
