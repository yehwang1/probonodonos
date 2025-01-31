"""
probonodonos post view.

URLs include:
/p/<postid_url_slug>/
"""
import arrow
import flask
import probonodonos


from probonodonos.views.helpers import (like, unlike, comment, uncomment,
                                    delete_post, check_ssesion)


def update_posts(posts, connection, logname):
    """Update_posts."""
    for post in posts:
        post["img_url"] = "/uploads/" + post.pop("filename")

        created = arrow.get(post.pop("created"), 'YYYY-MM-DD HH:mm:ss')
        present = arrow.utcnow()
        post["timestamp"] = created.humanize(present)

        owner_img = connection.execute(
            "SELECT filename "
            "FROM users "
            "WHERE username = ?", (post["owner"], )).fetchall()

        post["owner_img_url"] = "/uploads/" + owner_img[0]["filename"]

        post["comments"] = connection.execute(
            "SELECT commentid, owner, text "
            "FROM comments "
            "WHERE postid = ?", (post["postid"], )).fetchall()

        post["likes"] = connection.execute(
            "SELECT COUNT(postid) "
            "FROM likes "
            "WHERE postid = ?;",
            (post["postid"], )).fetchall()[0]["COUNT(postid)"]

        post["islike"] = connection.execute(
            "SELECT COUNT(1) "
            "FROM likes "
            "WHERE postid = ? and owner = ?;",
            (post["postid"], logname)).fetchall()[0]['COUNT(1)']


@probonodonos.app.route('/p/<postid_url_slug>/', methods=["GET", "POST"])
def show_post(postid_url_slug):
    """Display /p/<postid_url_slug>/ route."""
    logname, redirect = check_ssesion()
    if redirect:
        if flask.request.method == "POST":
            flask.abort(403)
        else:
            return redirect

    connection = probonodonos.model.get_db()

    if flask.request.method == "POST":
        dicts = flask.request.form

        if "like" in dicts.keys():
            postid = dicts["postid"]
            like(connection, postid, logname)
        elif "unlike" in dicts.keys():
            postid = dicts["postid"]
            unlike(connection, postid, logname)
        elif "comment" in dicts.keys():
            postid = dicts["postid"]
            text = dicts["text"]
            comment(connection, postid, text, logname)
        elif "uncomment" in dicts.keys():
            commentid = dicts["commentid"]
            uncomment(connection, commentid)
        elif "delete" in dicts.keys():
            postid = dicts["postid"]
            filename = delete_post(connection, postid)
            detete_file_path = probonodonos.config.UPLOAD_FOLDER / filename
            detete_file_path.unlink()

            return flask.redirect(
                flask.url_for("show_user", user_url_slug=logname))

    cur = connection.execute("SELECT * FROM posts WHERE postid = ?;",
                             (postid_url_slug, ))
    posts = cur.fetchall()

    update_posts(posts, connection, logname)

    # Add database info to context
    context = {"logname": logname}
    if len(posts) > 0:
        context.update(posts[0])

    return flask.render_template(
        "post.html", **context
    )  # this equals to flask.render_template("index.html", users = users)
