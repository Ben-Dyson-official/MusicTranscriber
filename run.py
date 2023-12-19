from App import app, db
from App.models import User, Piece

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Piece': Piece}