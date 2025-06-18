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

with app.app_context():
    # Ensure topics exist
    topic_titles = [
        ('Основы HTML', 'Узнайте о тегах HTML, атрибутах и семантических элементах...'),
        ('Основы CSS', 'Изучите свойства CSS, селекторы и макеты...'),
        ('Отзывчивый дизайн', 'Изучите медиа-запросы и гибкий контент...'),
        ('Основы JavaScript', 'Погрузитесь в основы программирования на JavaScript: переменные, функции, события и работа с DOM...'),
        ('Основы Python', 'Освойте основы программирования на Python: переменные, циклы, функции и структуры данных...')
    ]

    for title, content in topic_titles:
        if not Topic.query.filter_by(title=title).first():
            topic = Topic(title=title, content=content)
            db.session.add(topic)
    db.session.commit()

    # Add lessons for each topic
    html_topic = Topic.query.filter_by(title='Основы HTML').first()
    if html_topic and not Lesson.query.filter_by(topic_id=html_topic.id).first():
        html_lessons = [
            Lesson(title='Введение в HTML', description='Узнайте, что такое HTML и как он используется для создания веб-страниц.', topic_id=html_topic.id),
            Lesson(title='Структура HTML-документа', description='Изучите базовую структуру HTML-документа: теги <!DOCTYPE>, <html>, <head>, <body>.', topic_id=html_topic.id),
            Lesson(title='Теги и атрибуты', description='Познакомьтесь с основными тегами и их атрибутами для создания контента.', topic_id=html_topic.id),
            Lesson(title='Работа с текстом', description='Научитесь форматировать текст с помощью тегов <p>, <h1>-<h6>, <strong>, <em>.', topic_id=html_topic.id),
            Lesson(title='Списки в HTML', description='Создавайте упорядоченные и неупорядоченные списки с тегами <ul>, <ol>, <li>.', topic_id=html_topic.id),
            Lesson(title='Ссылки и навигация', description='Изучите, как создавать гиперссылки с тегом <a> и атрибутом href.', topic_id=html_topic.id),
            Lesson(title='Изображения', description='Добавляйте изображения на страницу с помощью тега <img> и его атрибутов.', topic_id=html_topic.id),
            Lesson(title='Таблицы', description='Создавайте таблицы с тегами <table>, <tr>, <td>, <th> для структурированных данных.', topic_id=html_topic.id),
            Lesson(title='Семантический HTML', description='Используйте семантические теги <header>, <footer>, <article>, <section> для улучшения структуры.', topic_id=html_topic.id),
            Lesson(title='Формы в HTML', description='Создавайте интерактивные формы с тегами <form>, <input>, <textarea>, <button>.', topic_id=html_topic.id),
        ]
        db.session.add_all(html_lessons)

    css_topic = Topic.query.filter_by(title='Основы CSS').first()
    if css_topic and not Lesson.query.filter_by(topic_id=css_topic.id).first():
        css_lessons = [
            Lesson(title='Введение в CSS', description='Познакомьтесь с CSS и его ролью в стилизации веб-страниц.', topic_id=css_topic.id),
            Lesson(title='Селекторы CSS', description='Изучите, как использовать селекторы для выбора элементов на странице.', topic_id=css_topic.id),
            Lesson(title='Свойства стилей', description='Научитесь применять стили для текста, фона, границ и других элементов.', topic_id=css_topic.id),
            Lesson(title='Модель коробки', description='Поймите, как работает box model: margin, padding, border.', topic_id=css_topic.id),
            Lesson(title='Позиционирование', description='Освойте способы размещения элементов с помощью position, float и flex.', topic_id=css_topic.id),
        ]
        db.session.add_all(css_lessons)

    responsive_topic = Topic.query.filter_by(title='Отзывчивый дизайн').first()
    if responsive_topic and not Lesson.query.filter_by(topic_id=responsive_topic.id).first():
        responsive_lessons = [
            Lesson(title='Введение в адаптивный дизайн', description='Узнайте, что такое адаптивный дизайн и зачем он нужен.', topic_id=responsive_topic.id),
            Lesson(title='Медиа-запросы', description='Изучите, как использовать медиа-запросы для адаптации под разные устройства.', topic_id=responsive_topic.id),
            Lesson(title='Гибкие макеты', description='Научитесь создавать гибкие макеты с помощью flexbox и grid.', topic_id=responsive_topic.id),
            Lesson(title='Адаптивные изображения', description='Освойте техники для работы с изображениями на разных экранах.', topic_id=responsive_topic.id),
            Lesson(title='Мобильная оптимизация', description='Изучите лучшие практики для улучшения мобильного опыта.', topic_id=responsive_topic.id),
        ]
        db.session.add_all(responsive_lessons)

    js_topic = Topic.query.filter_by(title='Основы JavaScript').first()
    if js_topic and not Lesson.query.filter_by(topic_id=js_topic.id).first():
        js_lessons = [
            Lesson(title='Введение в JavaScript', description='Познакомьтесь с JavaScript и его ролью в веб-разработке.', topic_id=js_topic.id),
            Lesson(title='Переменные и типы данных', description='Изучите, как объявлять переменные и работать с типами данных.', topic_id=js_topic.id),
            Lesson(title='Функции', description='Научитесь создавать и использовать функции в JavaScript.', topic_id=js_topic.id),
            Lesson(title='События', description='Освойте обработку событий для интерактивных страниц.', topic_id=js_topic.id),
            Lesson(title='Работа с DOM', description='Узнайте, как манипулировать элементами страницы с помощью DOM.', topic_id=js_topic.id),
        ]
        db.session.add_all(js_lessons)

    python_topic = Topic.query.filter_by(title='Основы Python').first()
    if python_topic and not Lesson.query.filter_by(topic_id=python_topic.id).first():
        python_lessons = [
            Lesson(title='Введение в Python', description='Познакомьтесь с Python и его возможностями для программирования.', topic_id=python_topic.id),
            Lesson(title='Переменные и типы данных', description='Изучите, как работать с переменными и основными типами данных.', topic_id=python_topic.id),
            Lesson(title='Условные операторы', description='Научитесь использовать if, elif, else для управления логикой.', topic_id=python_topic.id),
            Lesson(title='Циклы', description='Освойте циклы for и while для повторяющихся задач.', topic_id=python_topic.id),
            Lesson(title='Функции', description='Изучите, как создавать и использовать функции в Python.', topic_id=python_topic.id),
        ]
        db.session.add_all(python_lessons)

    db.session.commit()
    print("Уроки успешно добавлены в базу данных!")