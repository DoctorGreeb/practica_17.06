from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)

with app.app_context():
    # Check if topic with id=3 already exists
    if Topic.query.get(3):
        print("Ошибка: Тема с id=3 уже существует. Выберите другой id.")
    else:
        # Update topic_id in Lesson
        lessons = Lesson.query.filter_by(topic_id=6).all()
        for lesson in lessons:
            lesson.topic_id = 3
        db.session.commit()

        # Update topic_id in Comment
        comments = Comment.query.filter_by(topic_id=6).all()
        for comment in comments:
            comment.topic_id = 3
        db.session.commit()

        # Update id in Topic
        topic = Topic.query.get(6)
        if topic:
            topic.id = 3
            db.session.commit()
            print("Тема и связанные уроки/комментарии успешно обновлены: id изменено с 6 на 3.")
        else:
            print("Ошибка: Тема с id=6 не найдена.")