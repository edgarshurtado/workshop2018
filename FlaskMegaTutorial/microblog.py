from app import app, db, cli
from app.translate import translate
from app.models import User, Post

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'translate': translate}
