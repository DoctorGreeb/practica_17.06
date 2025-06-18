from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# Инициализация приложения Flask и SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Определение моделей
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    comments = db.relationship('Comment', backref='user', lazy=True)

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    lessons = db.relationship('Lesson', backref='topic', lazy=True)
    comments = db.relationship('Comment', backref='topic', lazy=True)

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)  # Новое поле для обучающей информации
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)

def update_lessons():
    with app.app_context():
        # Удаление всех таблиц
        db.drop_all()
        print("Все таблицы удалены.")

        # Создание таблиц
        db.create_all()
        print("Таблицы созданы.")

        # Проверка, пуста ли таблица Topic
        if not Topic.query.first():
            # Создание тем
            topics = [
                Topic(title='Основы HTML', content='Узнайте о тегах HTML, атрибутах и семантических элементах...'),
                Topic(title='Основы CSS', content='Изучите свойства CSS, селекторы и макеты...'),
                Topic(title='Отзывчивый дизайн', content='Изучите медиа-запросы и гибкий контент...'),
                Topic(title='Основы JavaScript', content='Погрузитесь в основы программирования на JavaScript: переменные, функции, события и работа с DOM...'),
                Topic(title='Основы Python', content='Освойте основы программирования на Python: переменные, циклы, функции и структуры данных...')
            ]
            db.session.add_all(topics)
            db.session.commit()
            print("Тем добавлено:", len(topics))

            # Получение ID тем
            html_topic = Topic.query.filter_by(title='Основы HTML').first()
            css_topic = Topic.query.filter_by(title='Основы CSS').first()
            responsive_topic = Topic.query.filter_by(title='Отзывчивый дизайн').first()
            js_topic = Topic.query.filter_by(title='Основы JavaScript').first()
            python_topic = Topic.query.filter_by(title='Основы Python').first()

            # Наполнение уроков для HTML
            if html_topic and not Lesson.query.filter_by(topic_id=html_topic.id).first():
                html_lessons = [
                    Lesson(
                        title='Введение в HTML',
                        description='Узнайте, что такое HTML и как он используется для создания веб-страниц.',
                        content='HTML (HyperText Markup Language) — это язык разметки для создания веб-страниц. Он определяет структуру контента с помощью тегов. Пример: <br><pre>&lt;html&gt;\n  &lt;head&gt;\n    &lt;title&gt;Моя страница&lt;/title&gt;\n  &lt;/head&gt;\n  &lt;body&gt;\n    &lt;h1&gt;Привет, мир!&lt;/h1&gt;\n  &lt;/body&gt;\n&lt;/html&gt;</pre>',
                        topic_id=html_topic.id
                    ),
                    Lesson(
                        title='Структура HTML-документа',
                        description='Изучите базовую структуру HTML-документа: теги <html>, <head>, <body>.',
                        content='Каждый HTML-документ начинается с тега <html>. Внутри него находятся <head> (метаданные, заголовок) и <body> (видимый контент). Пример: <br><pre>&lt;!DOCTYPE html&gt;\n&lt;html&gt;\n  &lt;head&gt;\n    &lt;title&gt;Страница&lt;/title&gt;\n  &lt;/head&gt;\n  &lt;body&gt;\n    &lt;p&gt;Это параграф.&lt;/p&gt;\n  &lt;/body&gt;\n&lt;/html&gt;</pre>',
                        topic_id=html_topic.id
                    ),
                    Lesson(
                        title='Теги и атрибуты',
                        description='Познакомьтесь с основными тегами и их атрибутами для создания контента.',
                        content='Теги — это команды, заключенные в угловые скобки, например <p> для параграфа. Атрибуты добавляют свойства, например id или class. Пример: <br><pre>&lt;p id="intro"&gt;Введение&lt;/p&gt;\n&lt;a href="https://example.com"&gt;Ссылка&lt;/a&gt;</pre>',
                        topic_id=html_topic.id
                    ),
                    Lesson(
                        title='Работа с текстом',
                        description='Научитесь форматировать текст с помощью тегов <p>, <h1> до <h6>, <strong>, <em>.',
                        content='Для форматирования текста используйте: <h1>–<h6> для заголовков, <p> для параграфов, <strong> для жирного текста, <em> для курсива. Пример: <br><pre>&lt;h1&gt;Заголовок&lt;/h1&gt;\n&lt;p&gt;Это &lt;strong&gt;важный&lt;/strong&gt; и &lt;em&gt;курсивный&lt;/em&gt; текст.&lt;/p&gt;</pre>',
                        topic_id=html_topic.id
                    ),
                    Lesson(
                        title='Списки в HTML',
                        description='Создавайте упорядоченные и неупорядоченные списки с тегами <ul>, <ol>, <li>.',
                        content='Неупорядоченные списки создаются с <ul>, упорядоченные — с <ol>. Элементы списка — <li>. Пример: <br><pre>&lt;ul&gt;\n  &lt;li&gt;Пункт 1&lt;/li&gt;\n  &lt;li&gt;Пункт 2&lt;/li&gt;\n&lt;/ul&gt;\n&lt;ol&gt;\n  &lt;li&gt;Шаг 1&lt;/li&gt;\n  &lt;li&gt;Шаг 2&lt;/li&gt;\n&lt;/ol&gt;</pre>',
                        topic_id=html_topic.id
                    ),
                    Lesson(
                        title='Ссылки и навигация',
                        description='Изучите, как создавать гиперссылки с тегом <a> и атрибутом href.',
                        content='Тег <a> создает ссылки. Атрибут href указывает URL. Пример: <br><pre>&lt;a href="https://example.com"&gt;Перейти на сайт&lt;/a&gt;</pre>',
                        topic_id=html_topic.id
                    ),
                    Lesson(
                        title='Изображения',
                        description='Добавляйте изображения на страницу с помощью тега <img> и его атрибутов.',
                        content='Тег <img> добавляет изображения. Атрибуты src (путь) и alt (описание) обязательны. Пример: <br><pre>&lt;img src="image.jpg" alt="Описание изображения"&gt;</pre>',
                        topic_id=html_topic.id
                    ),
                    Lesson(
                        title='Таблицы',
                        description='Создавайте таблицы с тегами <table>, <tr>, <td>, <th> для структурированных данных.',
                        content='Тег <table> создает таблицу, <tr> — строку, <th> — заголовок ячейки, <td> — ячейку. Пример: <br><pre>&lt;table&gt;\n  &lt;tr&gt;\n    &lt;th&gt;Заголовок&lt;/th&gt;\n    &lt;th&gt;Данные&lt;/th&gt;\n  &lt;/tr&gt;\n  &lt;tr&gt;\n    &lt;td&gt;Ячейка 1&lt;/td&gt;\n    &lt;td&gt;Ячейка 2&lt;/td&gt;\n  &lt;/tr&gt;\n&lt;/table&gt;</pre>',
                        topic_id=html_topic.id
                    ),
                    Lesson(
                        title='Семантический HTML',
                        description='Используйте семантические теги <header>, <span>, <article>, <section> для улучшения структуры.',
                        content='Семантические теги, такие как <header>, <span>, <article>, <section>, делают код понятнее. Пример: <br><pre>&lt;header&gt;\n  &lt;nav a&gt;Главная&lt;/nav a&gt;\n&lt;/header&gt;\n&lt;section&gt;\n  &lt;article&gt;Статья&lt;/article&gt;\n&lt;/section&gt;</pre>',
                        topic_id=html_topic.id
                    ),
                    Lesson(
                        title='Формы в HTML',
                        description='Создавайте интерактивные формы с тегами <form>, <input>, <textarea>, <button>.',
                        content='Тег <form> создает форму, <input> — поля ввода, <textarea> — многострочный текст, <button> — кнопку. Пример: <br><pre>&lt;form action="/submit"&gt;\n  &lt;input type="text" name="username"&gt;\n  &lt;textarea name="comment"&gt;&lt;/textarea&gt;\n  &lt;button type="submit"&gt;Отправить&lt;/button&gt;\n&lt;/form&gt;</pre>',
                        topic_id=html_topic.id
                    ),
                ]
                db.session.add_all(html_lessons)
                print("Уроки для HTML добавлены:", len(html_lessons))

            # Наполнение уроков для CSS
            if css_topic and not Lesson.query.filter_by(topic_id=css_topic.id).first():
                css_lessons = [
                    Lesson(
                        title='Введение в CSS',
                        description='Познакомьтесь с CSS и его ролью в стилизации веб-страниц.',
                        content='CSS (Cascading Style Sheets) управляет внешним видом веб-страниц. Пример: <br><pre>h1 { color: blue; font-size: 24px; }</pre>',
                        topic_id=css_topic.id
                    ),
                    Lesson(
                        title='Селекторы CSS',
                        description='Изучите, как использовать селекторы для выбора элементов на странице.',
                        content='Селекторы выбирают элементы для стилизации: по тегу, классу (.class), ID (#id). Пример: <br><pre>.intro { background: #f0f0f0; }\n#title { font-weight: bold; }</pre>',
                        topic_id=css_topic.id
                    ),
                    Lesson(
                        title='Свойства стилей',
                        description='Научитесь применять стили для текста, фона, границ и других элементов.',
                        content='CSS-свойства: color, background, border, font-size и др. Пример: <br><pre>p { color: #333; background: yellow; border: 1px solid black; }</pre>',
                        topic_id=css_topic.id
                    ),
                    Lesson(
                        title='Модель коробки',
                        description='Поймите, как работает box model: margin, padding, border.',
                        content='Box model определяет размеры элемента: margin (внешний отступ), padding (внутренний отступ), border. Пример: <br><pre>div { margin: 10px; padding: 15px; border: 2px solid blue; }</pre>',
                        topic_id=css_topic.id
                    ),
                    Lesson(
                        title='Позиционирование',
                        description='Освойте способы размещения элементов с помощью position, float и flex.',
                        content='Свойство position (static, relative, absolute, fixed) управляет расположением. Flexbox упрощает макеты. Пример: <br><pre>.container { display: flex; justify-content: center; }\ndiv { position: absolute; top: 10px; }</pre>',
                        topic_id=css_topic.id
                    ),
                ]
                db.session.add_all(css_lessons)
                print("Уроки для CSS добавлены:", len(css_lessons))

            # Наполнение уроков для Отзывчивого дизайна
            if responsive_topic and not Lesson.query.filter_by(topic_id=responsive_topic.id).first():
                responsive_lessons = [
                    Lesson(
                        title='Введение в адаптивный дизайн',
                        description='Узнайте, что такое адаптивный дизайн и зачем он нужен.',
                        content='Адаптивный дизайн делает сайты удобными на разных устройствах. Используются медиа-запросы и гибкие макеты. Пример: <br><pre>@media (max-width: 600px) { body { font-size: 14px; } }</pre>',
                        topic_id=responsive_topic.id
                    ),
                    Lesson(
                        title='Медиа-запросы',
                        description='Изучите, как использовать медиа-запросы для адаптации под разные устройства.',
                        content='Медиа-запросы (@media) применяют стили в зависимости от условий (ширина экрана и др.). Пример: <br><pre>@media (min-width: 768px) { .container { width: 80%; } }</pre>',
                        topic_id=responsive_topic.id
                    ),
                    Lesson(
                        title='Гибкие макеты',
                        description='Научитесь создавать гибкие макеты с помощью flexbox и grid.',
                        content='Flexbox и CSS Grid создают адаптивные макеты. Пример Flexbox: <br><pre>.container { display: flex; flex-wrap: wrap; gap: 10px; }</pre><br>Пример Grid: <br><pre>.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); }</pre>',
                        topic_id=responsive_topic.id
                    ),
                    Lesson(
                        title='Адаптивные изображения',
                        description='Освойте техники для работы с изображениями на разных экранах.',
                        content='Используйте max-width: 100% или тег <picture> для адаптивных изображений. Пример: <br><pre>img { max-width: 100%; height: auto; }\n&lt;picture&gt;\n  &lt;source srcset="small.jpg" media="(max-width: 600px)"&gt;\n  &lt;img src="large.jpg" alt="Изображение"&gt;\n&lt;/picture&gt;</pre>',
                        topic_id=responsive_topic.id
                    ),
                    Lesson(
                        title='Мобильная оптимизация',
                        description='Изучите лучшие практики для улучшения мобильного опыта.',
                        content='Упрощайте навигацию, увеличивайте кнопки, оптимизируйте загрузку. Пример: <br><pre>button { padding: 15px; font-size: 16px; }\nmeta(name="viewport" content="width=device-width, initial-scale=1.0")</pre>',
                        topic_id=responsive_topic.id
                    ),
                ]
                db.session.add_all(responsive_lessons)
                print("Уроки для Отзывчивого дизайна добавлены:", len(responsive_lessons))

            # Наполнение уроков для JavaScript
            if js_topic and not Lesson.query.filter_by(topic_id=js_topic.id).first():
                js_lessons = [
                    Lesson(
                        title='Введение в JavaScript',
                        description='Познакомьтесь с JavaScript и его ролью в веб-разработке.',
                        content='JavaScript добавляет интерактивность веб-страницам. Пример: <br><pre>console.log("Привет, мир!");</pre>',
                        topic_id=js_topic.id
                    ),
                    Lesson(
                        title='Переменные и типы данных',
                        description='Изучите, как объявлять переменные и работать с типами данных.',
                        content='Переменные объявляются с let, const, var. Типы: строки, числа, массивы. Пример: <br><pre>let name = "Антон";\nconst age = 25;\nlet numbers = [1, 2, 3];</pre>',
                        topic_id=js_topic.id
                    ),
                    Lesson(
                        title='Функции',
                        description='Научитесь создавать и использовать функции в JavaScript.',
                        content='Функции выполняют задачи. Пример: <br><pre>function greet(name) {\n  return "Привет, " + name;\n}\nconsole.log(greet("Антон"));</pre>',
                        topic_id=js_topic.id
                    ),
                    Lesson(
                        title='События',
                        description='Освойте обработку событий для интерактивных страниц.',
                        content='События, такие как клик, обрабатываются с addEventListener. Пример: <br><pre>document.querySelector("button").addEventListener("click", () => {\n  alert("Кнопка нажата!");\n});</pre>',
                        topic_id=js_topic.id
                    ),
                    Lesson(
                        title='Работа с DOM',
                        description='Узнайте, как манипулировать элементами страницы с помощью JavaScript.',
                        content='DOM позволяет изменять HTML. Пример: <br><pre>document.querySelector("#title").textContent = "Новый заголовок";</pre>',
                        topic_id=js_topic.id
                    ),
                ]
                db.session.add_all(js_lessons)
                print("Уроки для JavaScript добавлены:", len(js_lessons))

            # Наполнение для Python
            if python_topic and not Lesson.query.filter_by(topic_id=python_topic.id).first():
                python_lessons = [
                    Lesson(
                        title='Введение в Python',
                        description='Познакомьтесь с Python и его возможностями для программирования.',
                        content='Python — простой и мощный язык программирования. Пример: <br><pre>print("Привет, мир!")</pre>',
                        topic_id=python_topic.id
                    ),
                    Lesson(
                        title='Переменные и типы данных',
                        description='Изучите, как работать с переменными и основными типами данных.',
                        content='Переменные в Python не требуют явного объявления типа. Пример: <br><pre>name = "Антон"\nage = 25\nnumbers = [1, 2, 3]</pre>',
                        topic_id=python_topic.id
                    ),
                    Lesson(
                        title='Условные операторы',
                        description='Научитесь использовать if, elif, else для управления логикой.',
                        content='Условные операторы управляют выполнением кода. Пример: <br><pre>age = 18\nif age >= 18:\n    print("Совершеннолетний")\nelse:\n    print("Несовершеннолетний")</pre>',
                        topic_id=python_topic.id
                    ),
                    Lesson(
                        title='Циклы',
                        description='Освойте циклы for и while для повторяющихся задач.',
                        content='Циклы автоматизируют повторения. Пример: <br><pre>for i in range(5):\n    print(i)\n# или\nwhile i < 5:\n    print(i)\n    i += 1</pre>',
                        topic_id=python_topic.id
                    ),
                    Lesson(
                        title='Функции',
                        description='Изучите, как создавать и использовать функции в Python.',
                        content='Функции определяются с помощью def. Пример: <br><pre>def greet(name):\n    return f"Привет, {name}"\nprint(greet("Антон"))</pre>',
                        topic_id=python_topic.id
                    ),
                ]
                db.session.add_all(python_lessons)
                print("Уроки для Python добавлены:", len(python_lessons))

            db.session.commit()
            print("База данных успешно наполнена.")

if __name__ == '__main__':
    update_lessons()