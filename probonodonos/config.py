"""probonodonos development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = (b'\x8d\xa3<\xd9\xb9\x83\x889$\xd2\x14\xe3\xeb\x03Y'
              b'\xa1+0\x10\x15\xe7\xbb\x1e\xa2')
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
probonodonos_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = probonodonos_ROOT / 'var' / 'uploads'
STATIC_FOLDER = probonodonos_ROOT / 'probonodonos' / 'static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/probonodonos.sqlite3
DATABASE_FILENAME = probonodonos_ROOT / 'var' / 'probonodonos.sqlite3'
