from app import create_app, db
from app.models import User, Event, NewsPost, GalleryItem

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Event': Event,
        'NewsPost': NewsPost,
        'GalleryItem': GalleryItem
    }

if __name__ == '__main__':
    app.run(debug=True) 