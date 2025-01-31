"""
probonodonos index (main) view.

URLs include:
/
"""
import flask
import probonodonos

from probonodonos.views.helpers import like, unlike, comment, check_ssesion
from probonodonos.views.post import update_posts


@probonodonos.app.route('/', methods=["GET", "POST"])
def show_index():
    """Display / route."""
    logname, redirect = check_ssesion()
    if redirect:
        return redirect

    # Connect to database
    connection = probonodonos.model.get_db()

    if flask.request.method == "POST":
        dicts = flask.request.form
        postid = dicts["postid"]
        if "like" in dicts.keys():
            like(connection, postid, logname)
        elif "unlike" in dicts.keys():
            unlike(connection, postid, logname)
        elif "comment" in dicts.keys():
            text = dicts["text"]
            comment(connection, postid, text, logname)
    cur = connection.execute(
        "SELECT username FROM users")
    following_dic = cur.fetchall()
    index_people = [i["username"] for i in following_dic
                    ]  # people that logname MAN is following
    index_people.append(logname)  # posts in index are from following and MAN

    cur = connection.execute("SELECT * FROM posts ORDER BY postid DESC;")
    posts_dic = cur.fetchall()

    posts = [post for post in posts_dic if post["owner"] in index_people]

    update_posts(posts, connection, logname)

    # Add database info to context
    context = {"logname": logname, "posts": posts}

    return flask.render_template(
        "index.html", **context
    )  # this equals to flask.render_template("index.html", users = users)
