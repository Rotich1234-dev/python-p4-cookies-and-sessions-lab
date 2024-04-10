from flask import Flask, jsonify, session
from flask_migrate import Migrate

from models import db, Article

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles/<int:id>')
def show_article(id):
    session['page_views'] = session.get('page_views', 0)

    # Increment page_views for each request
    session['page_views'] += 1

    # Check if page_views exceeds limit
    if session['page_views'] <= 3:
        # Fetch article data from the database
        article = Article.query.get(id)
        if article:
            # Return article data
            return jsonify(article.serialize()), 200
        else:
            # Return error if article not found
            return jsonify({'message': 'Article not found'}), 404
    else:
        # Return 401 if page_views exceeds limit
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

if __name__ == '__main__':
    app.run(port=5555)
