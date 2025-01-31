"""Views, one for each probonodonos page."""
import flask
import probonodonos

from probonodonos.views.index import show_index
from probonodonos.views.post import show_post
from probonodonos.views.explore import show_explore
from probonodonos.views.user import show_user
from probonodonos.views.followers import show_followers
from probonodonos.views.following import show_following
from probonodonos.views.login import login
from probonodonos.views.edit import edit
from probonodonos.views.create import create
from probonodonos.views.logout import logout
from probonodonos.views.password import password
from probonodonos.views.delete import delete


@probonodonos.app.route('/uploads/<path:filename>')
def download_file(filename):
    """Download_file."""
    # static file permission
    if "user" not in flask.session:
        flask.abort(403)

    return flask.send_from_directory(probonodonos.app.config['UPLOAD_FOLDER'],
                                     filename,
                                     as_attachment=True)


# flask ---- Static Files
# https://flask.palletsprojects.com/en/1.1.x/quickstart/#static-files
