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
    content = db.Column(db.Text, nullable=False)
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
                Topic(title='Основы HTML', content='Узнайте о тегах HTML, атрибутах и семантических элементах для создания веб-страниц.'),
                Topic(title='Основы CSS', content='Изучите свойства CSS, селекторы и макеты для стилизации страниц.'),
                Topic(title='Отзывчивый дизайн', content='Освойте медиа-запросы, гибкие макеты и адаптивные изображения.'),
                Topic(title='Основы JavaScript', content='Погрузитесь в программирование на JavaScript: переменные, функции, события.'),
                Topic(title='Основы Python', content='Изучите Python: переменные, циклы, функции и структуры данных.')
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
                        content='<p>HTML (HyperText Markup Language) — стандартный язык разметки для создания веб-страниц. Он определяет структуру контента с помощью тегов, которые браузеры интерпретируют для отображения текста, изображений и ссылок. HTML — основа веб-разработки, работающая вместе с CSS и JavaScript.</p><ul><li><strong>Теги</strong>: Элементы, такие как <code>&lt;p&gt;</code>, <code>&lt;h1&gt;</code>, задают тип контента.</li><li><strong>Атрибуты</strong>: Добавляют свойства, например, <code>id</code>, <code>href</code>.</li><li><strong>Семантика</strong>: HTML5 использует теги вроде <code>&lt;header&gt;</code> для улучшения SEO.</li></ul><h3>Пример кода</h3><pre><code>&lt;!DOCTYPE html&gt;\n&lt;html lang="ru"&gt;\n  &lt;head&gt;\n    &lt;meta charset="UTF-8"&gt;\n    &lt;title&gt;Моя страница&lt;/title&gt;\n  &lt;/head&gt;\n  &lt;body&gt;\n    &lt;h1&gt;Привет, мир!&lt;/h1&gt;\n    &lt;p&gt;Это моя первая страница.&lt;/p&gt;\n  &lt;/body&gt;\n&lt;/html&gt;\n</code></pre><h3>Объяснение</h3><ol><li><code>&lt;!DOCTYPE html&gt;</code>: Указывает стандарт HTML5.</li><li><code>&lt;html lang="ru"&gt;</code>: Задает язык документа.</li><li><code>&lt;head&gt;</code>: Содержит метаданные.</li><li><code>&lt;body&gt;</code>: Видимый контент.</li></ol><p>Сохраните код в файл <code>.html</code> и откройте в браузере. Тестируйте с DevTools для отладки.</p>',
                        topic_id=html_topic.id
                    ),
                    Lesson(
                        title='Структура HTML-документа',
                        description='Изучите базовую структуру HTML-документа: теги <html>, <head>, <body>.',
                        content='<p>HTML-документ имеет четкую структуру, включающую <code>&lt;!DOCTYPE html&gt;</code>, <code>&lt;html&gt;</code>, <code>&lt;head&gt;</code> и <code>&lt;body&gt;</code>. Это обеспечивает правильное отображение в браузерах.</p><ul><li><strong>Метаданные</strong>: В <code>&lt;head&gt;</code> задаются кодировка, заголовок, стили.</li><li><strong>Контент</strong>: В <code>&lt;body&gt;</code> размещается видимый контент.</li></ul><h3>Пример кода</h3><pre><code>&lt;!DOCTYPE html&gt;\n&lt;html lang="ru"&gt;\n  &lt;head&gt;\n    &lt;meta charset="UTF-8"&gt;\n    &lt;title&gt;Структура&lt;/title&gt;\n  &lt;/head&gt;\n  &lt;body&gt;\n    &lt;header&gt;\n      &lt;h1&gt;Добро пожаловать&lt;/h1&gt;\n    &lt;/header&gt;\n    &lt;main&gt;\n      &lt;p&gt;Контент.&lt;/p&gt;\n    &lt;/main&gt;\n  &lt;/body&gt;\n&lt;/html&gt;\n</code></pre><h3>Объяснение</h3><ol><li><code>&lt;!DOCTYPE html&gt;</code>: Объявляет HTML5.</li><li><code>&lt;meta charset="UTF-8"&gt;</code>: Задает кодировку.</li><li><code>&lt;header&gt;</code>, <code>&lt;main&gt;</code>: Семантические теги.</li></ol><p>Используйте семантику для SEO и тестируйте в DevTools.</p>',
                        topic_id=html_topic.id
                    ),
                    Lesson(
                        title='Теги и атрибуты',
                        description='Познакомьтесь с основными тегами и их атрибутами для создания контента.',
                        content='<p>Теги в HTML задают тип контента, а атрибуты — их свойства. Например, <code>&lt;a&gt;</code> создает ссылку, а атрибут <code>href</code> указывает URL.</p><ul><li><strong>Парные теги</strong>: Содержат контент, например, <code>&lt;p&gt;...&lt;/p&gt;</code>.</li><li><strong>Одиночные теги</strong>: Например, <code>&lt;img&gt;</code>.</li><li><strong>Атрибуты</strong>: <code>id</code>, <code>class</code>, <code>src</code>.</li></ul><h3>Пример кода</h3><pre><code>&lt;div id="main"&gt;\n  &lt;p class="intro"&gt;Текст&lt;/p&gt;\n  &lt;a href="https://example.com"&gt;Ссылка&lt;/a&gt;\n  &lt;img src="photo.jpg" alt="Фото"&gt;\n&lt;/div&gt;\n</code></pre><h3>Объяснение</h3><ol><li><code>&lt;div&gt;</code>: Контейнер для группировки.</li><li><code>id</code>, <code>class</code>: Для стилизации.</li><li><code>href</code>, <code>src</code>, <code>alt</code>: Задают функциональность.</li></ol><p>Тестируйте ссылки и изображения в браузере.</p>',
                        topic_id=html_topic.id
                    ),
                    Lesson(
                        title='Работа с текстом',
                        description='Научитесь форматировать текст с помощью тегов <p>, <h1>–<h6>, <strong>, <em>.',
                        content='<p>HTML предоставляет теги для структурирования текста, такие как заголовки и параграфы, а также для выделения важных частей.</p><ul><li><strong>Заголовки</strong>: <code>&lt;h1&gt;</code>–<code>&lt;h6&gt;</code> для иерархии.</li><li><strong>Выделение</strong>: <code>&lt;strong&gt;</code> для жирного, <code>&lt;em&gt;</code> для курсива.</li></ul><h3>Пример кода</h3><pre><code>&lt;h1&gt;Главный заголовок&lt;/h1&gt;\n&lt;p&gt;Это &lt;strong&gt;важный&lt;/strong&gt; и &lt;em&gt;курсивный&lt;/em&gt; текст.&lt;/p&gt;\n</code></pre><h3>Объяснение</h3><ol><li><code>&lt;h1&gt;</code>: Основной заголовок.</li><li><code>&lt;strong&gt;</code>: Семантически важный текст.</li><li><code>&lt;em&gt;</code>: Акцент.</li></ol><p>Стилизуйте текст с CSS и проверяйте в DevTools.</p>',
                        topic_id=html_topic.id
                    ),
                    Lesson(
                        title='Списки в HTML',
                        description='Создавайте списки с тегами <ul>, <ol>, <li> для структурированных данных.',
                        content='<p>Списки в HTML организуют информацию, делая ее более читаемой.</p><ul><li><strong>Неупорядоченные</strong>: <code>&lt;ul&gt;</code> с маркерами.</li><li><strong>Упорядоченные</strong>: <code>&lt;ol&gt;</code> с номерами.</li></ul><h3>Пример кода</h3><pre><code>&lt;ul&gt;\n  &lt;li&gt;Яблоки&lt;/li&gt;\n  &lt;li&gt;Груши&lt;/li&gt;\n&lt;/ul&gt;\n&lt;ol&gt;\n  &lt;li&gt;Шаг 1&lt;/li&gt;\n  &lt;li&gt;Шаг 2&lt;/li&gt;\n&lt;/ol&gt;\n</code></pre><h3>Объяснение</h3><ol><li><code>&lt;ul&gt;</code>: Для ненумерованных списков.</li><li><code>&lt;ol&gt;</code>: Для нумерованных списков.</li><li><code>&lt;li&gt;</code>: Элемент списка.</li></ol><p>Стилизуйте списки с CSS для кастомных маркеров.</p>',
                        topic_id=html_topic.id
                    ),
                    Lesson(
                        title='Ссылки и навигация',
                        description='Изучите создание гиперссылок с тегом <a> и атрибутом href.',
                        content='<p>Гиперссылки позволяют пользователям переходить между страницами или разделами.</p><ul><li><strong>Внешние ссылки</strong>: Указывают URL.</li><li><strong>Внутренние</strong>: Ссылаются на ID элемента.</li></ul><h3>Пример кода</h3><pre><code>&lt;nav&gt;\n  &lt;a href="https://example.com"&gt;Сайт&lt;/a&gt;\n  &lt;a href="#footer"&gt;Футер&lt;/a&gt;\n&lt;/nav&gt;\n&lt;div id="footer"&gt;Конец&lt;/div&gt;\n</code></pre><h3>Объяснение</h3><ol><li><code>&lt;nav&gt;</code>: Семантический тег для навигации.</li><li><code>href</code>: Задает адрес.</li></ol><p>Тестируйте переходы и используйте <code>target="_blank"</code> для новых вкладок.</p>',
                        topic_id=html_topic.id
                    ),
                    Lesson(
                        title='Изображения',
                        description='Добавляйте изображения с тегом <img> и атрибутами src, alt.',
                        content='<p>Изображения улучшают визуальный опыт, добавляясь с помощью <code>&lt;img&gt;</code>.</p><ul><li><strong>Обязательные атрибуты</strong>: <code>src</code> и <code>alt</code>.</li><li><strong>Адаптивность</strong>: Используйте CSS или <code>&lt;picture&gt;</code>.</li></ul><h3>Пример кода</h3><pre><code>&lt;img src="photo.jpg" alt="Пейзаж" width="300"&gt;\n&lt;picture&gt;\n  &lt;source srcset="small.jpg" media="(max-width: 600px)"&gt;\n  &lt;img src="large.jpg" alt="Пейзаж"&gt;\n&lt;/picture&gt;\n</code></pre><h3>Объяснение</h3><ol><li><code>src</code>: Путь к изображению.</li><li><code>alt</code>: Текст для доступности.</li><li><code>&lt;picture&gt;</code>: Для адаптивных изображений.</li></ol><p>Оптимизируйте изображения для скорости загрузки.</p>',
                        topic_id=html_topic.id
                    ),
                    Lesson(
                        title='Таблицы',
                        description='Создавайте таблицы с <table>, <tr>, <td>, <th> для данных.',
                        content='<p>Таблицы структурируют данные, такие как расписания или результаты.</p><ul><li><strong>Структура</strong>: <code>&lt;tr&gt;</code> для строк, <code>&lt;td&gt;</code> для ячеек.</li><li><strong>Заголовки</strong>: <code>&lt;th&gt;</code> для ячеек заголовков.</li></ul><h3>Пример кода</h3><pre><code>&lt;table border="1"&gt;\n  &lt;tr&gt;\n    &lt;th&gt;Имя&lt;/th&gt;\n    &lt;th&gt;Возраст&lt;/th&gt;\n  &lt;/tr&gt;\n  &lt;tr&gt;\n    &lt;td&gt;Антон&lt;/td&gt;\n    &lt;td&gt;25&lt;/td&gt;\n  &lt;/tr&gt;\n&lt;/table&gt;\n</code></pre><h3>Объяснение</h3><ol><li><code>&lt;table&gt;</code>: Контейнер таблицы.</li><li><code>&lt;th&gt;</code>: Заголовок.</li><li><code>border</code>: Визуальная граница.</li></ol><p>Стилизуйте с CSS и используйте <code>&lt;thead&gt;</code> для семантики.</p>',
                        topic_id=html_topic.id
                    ),
                    Lesson(
                        title='Семантический HTML',
                        description='Используйте <header>, <footer>, <article> для структуры.',
                        content='<p>Семантические теги улучшают читаемость и SEO, описывая назначение контента.</p><ul><li><strong>Примеры</strong>: <code>&lt;header&gt;</code>, <code>&lt;footer&gt;</code>, <code>&lt;article&gt;</code>.</li><li><strong>Доступность</strong>: Упрощают работу скринридеров.</li></ul><h3>Пример кода</h3><pre><code>&lt;header&gt;\n  &lt;nav&gt;\n    &lt;a href="/"&gt;Главная&lt;/a&gt;\n  &lt;/nav&gt;\n&lt;/header&gt;\n&lt;main&gt;\n  &lt;article&gt;\n    &lt;h2&gt;Статья&lt;/h2&gt;\n    &lt;p&gt;Текст...&lt;/p&gt;\n  &lt;/article&gt;\n&lt;/main&gt;\n</code></pre><h3>Объяснение</h3><ol><li><code>&lt;header&gt;</code>: Шапка страницы.</li><li><code>&lt;article&gt;</code>: Самостоятельный контент.</li></ol><p>Избегайте избыточных <code>&lt;div&gt;</code>.</p>',
                        topic_id=html_topic.id
                    ),
                    Lesson(
                        title='Формы в HTML',
                        description='Создавайте формы с <form>, <input>, <textarea>, <button>.',
                        content='<p>Формы собирают данные пользователей, такие как регистрационные данные.</p><ul><li><strong>Элементы</strong>: <code>&lt;input&gt;</code>, <code>&lt;textarea&gt;</code>.</li><li><strong>Атрибуты</strong>: <code>name</code>, <code>required</code>.</li></ul><h3>Пример кода</h3><pre><code>&lt;form action="/submit" method="POST"&gt;\n  &lt;label for="name"&gt;Имя:&lt;/label&gt;\n  &lt;input type="text" id="name" name="username" required&gt;\n  &lt;textarea name="comment"&gt;&lt;/textarea&gt;\n  &lt;button type="submit"&gt;Отправить&lt;/button&gt;\n&lt;/form&gt;\n</code></pre><h3>Объяснение</h3><ol><li><code>action</code>: URL для отправки.</li><li><code>method</code>: Метод (POST/GET).</li><li><code>&lt;label&gt;</code>: Для доступности.</li></ol><p>Тестируйте отправку и валидацию.</p>',
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
                        description='Познакомьтесь с CSS и его ролью в стилизации.',
                        content='<p>CSS (Cascading Style Sheets) управляет внешним видом веб-страниц: цвета, шрифты, макеты.</p><ul><li><strong>Подключение</strong>: Через <code>&lt;link&gt;</code> или <code>&lt;style&gt;</code>.</li><li><strong>Каскадность</strong>: Правила приоритета стилей.</li></ul><h3>Пример кода</h3><pre><code>h1 {\n  color: blue;\n  font-size: 24px;\n}\n.container {\n  background: #f0f0f0;\n  padding: 20px;\n}\n</code></pre><h3>Объяснение</h3><ol><li><code>h1</code>: Селектор тега.</li><li><code>.container</code>: Селектор класса.</li><li><code>padding</code>: Внутренний отступ.</li></ol><p>Тестируйте стили в DevTools.</p>',
                        topic_id=css_topic.id
                    ),
                    Lesson(
                        title='Селекторы CSS',
                        description='Изучите селекторы для выбора элементов.',
                        content='<p>Селекторы определяют, к каким элементам применяются стили.</p><ul><li><strong>Типы</strong>: Теговые, классовые, ID, псевдоклассы.</li><li><strong>Специфичность</strong>: ID > класс > тег.</li></ul><h3>Пример кода</h3><pre><code>#title {\n  color: blue;\n}\n.container p {\n  font-size: 16px;\n}\n.button:hover {\n  background: #ff0;\n}\n</code></pre><h3>Объяснение</h3><ol><li><code>#title</code>: Селектор ID.</li><li><code>:hover</code>: Псевдокласс.</li></ol><p>Проверяйте специфичность в DevTools.</p>',
                        topic_id=css_topic.id
                    ),
                    Lesson(
                        title='Свойства стилей',
                        description='Применяйте стили для текста, фона, границ.',
                        content='<p>CSS-свойства изменяют внешний вид элементов.</p><ul><li><strong>Текст</strong>: <code>color</code>, <code>font-size</code>.</li><li><strong>Фон</strong>: <code>background-color</code>.</li></ul><h3>Пример кода</h3><pre><code>p {\n  color: #333;\n  font-family: Arial;\n}\n.box {\n  background: #f0f0f0;\n  border: 2px solid blue;\n}\n</code></pre><h3>Объяснение</h3><ol><li><code>font-family</code>: Шрифт.</li><li><code>border</code>: Граница.</li></ol><p>Используйте сокращенные записи, например, <code>border</code>.</p>',
                        topic_id=css_topic.id
                    ),
                    Lesson(
                        title='Модель коробки',
                        description='Поймите box model: margin, padding, border.',
                        content='<p>Box model определяет пространство элемента.</p><ul><li><strong>Состав</strong>: Контент, padding, border, margin.</li><li><strong>Box-sizing</strong>: Управляет расчетом размеров.</li></ul><h3>Пример кода</h3><pre><code>.box {\n  width: 200px;\n  padding: 20px;\n  border: 5px solid #000;\n  box-sizing: border-box;\n}\n</code></pre><h3>Объяснение</h3><ol><li><code>padding</code>: Внутренний отступ.</li><li><code>box-sizing: border-box</code>: Упрощает расчет.</li></ol><p>Тестируйте размеры в DevTools.</p>',
                        topic_id=css_topic.id
                    ),
                    Lesson(
                        title='Позиционирование',
                        description='Освойте position, float, flex для размещения.',
                        content='<p>Позиционирование управляет расположением элементов.</p><ul><li><strong>Position</strong>: <code>relative</code>, <code>absolute</code>.</li><li><strong>Flexbox</strong>: <code>display: flex</code>.</li></ul><h3>Пример кода</h3><pre><code>.container {\n  display: flex;\n  justify-content: space-between;\n}\n.fixed {\n  position: fixed;\n  top: 10px;\n}\n</code></pre><h3>Объяснение</h3><ol><li><code>flex</code>: Гибкий макет.</li><li><code>fixed</code>: Фиксированное положение.</li></ol><p>Проверяйте адаптивность в DevTools.</p>',
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
                        description='Узнайте, что такое адаптивный дизайн.',
                        content='<p>Адаптивный дизайн обеспечивает удобство сайтов на любых устройствах.</p><ul><li><strong>Гибкость</strong>: Используйте %, vw, rem.</li><li><strong>Медиа-запросы</strong>: Адаптация под размеры экрана.</li></ul><h3>Пример кода</h3><pre><code>&lt;meta name="viewport" content="width=device-width, initial-scale=1.0"&gt;\n&lt;style&gt;\n.container {\n  width: 90%;\n}\n@media (max-width: 600px) {\n  .container {\n    font-size: 14px;\n  }\n}\n&lt;/style&gt;\n</code></pre><h3>Объяснение</h3><ol><li><code>viewport</code>: Для мобильных устройств.</li><li><code>@media</code>: Условие стилей.</li></ol><p>Тестируйте в DevTools, переключая размеры экрана.</p>',
                        topic_id=responsive_topic.id
                    ),
                    Lesson(
                        title='Медиа-запросы',
                        description='Используйте медиа-запросы для адаптации.',
                        content='<p>Медиа-запросы изменяют стили в зависимости от условий, таких как ширина экрана.</p><ul><li><strong>Условия</strong>: <code>max-width</code>, <code>min-width</code>.</li><li><strong>Mobile-first</strong>: Используйте <code>min-width</code>.</li></ul><h3>Пример кода</h3><pre><code>body {\n  font-size: 16px;\n}\n@media (min-width: 768px) {\n  body {\n    font-size: 18px;\n  }\n}\n</code></pre><h3>Объяснение</h3><ol><li><code>@media</code>: Условие для стилей.</li><li><code>min-width</code>: Стили для больших экранов.</li></ol><p>Группируйте запросы для оптимизации.</p>',
                        topic_id=responsive_topic.id
                    ),
                    Lesson(
                        title='Гибкие макеты',
                        description='Создавайте макеты с flexbox и grid.',
                        content='<p>Flexbox и Grid создают адаптивные макеты.</p><ul><li><strong>Flexbox</strong>: Для одномерных макетов.</li><li><strong>Grid</strong>: Для двумерных сеток.</li></ul><h3>Пример кода</h3><pre><code>.container {\n  display: flex;\n  flex-wrap: wrap;\n  gap: 10px;\n}\n.grid {\n  display: grid;\n  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));\n}\n</code></pre><h3>Объяснение</h3><ol><li><code>flex-wrap</code>: Перенос элементов.</li><li><code>grid-template-columns</code>: Адаптивная сетка.</li></ol><p>Тестируйте адаптивность в DevTools.</p>',
                        topic_id=responsive_topic.id
                    ),
                    Lesson(
                        title='Адаптивные изображения',
                        description='Работайте с изображениями для разных экранов.',
                        content='<p>Адаптивные изображения подстраиваются под размер экрана.</p><ul><li><strong>Техники</strong>: <code>max-width</code>, <code>&lt;picture&gt;</code>.</li><li><strong>Форматы</strong>: WebP для оптимизации.</li></ul><h3>Пример кода</h3><pre><code>&lt;img src="default.jpg" srcset="small.jpg 480w" sizes="(max-width: 600px) 480px" alt="Картина"&gt;\n&lt;picture&gt;\n  &lt;source srcset="image.webp" type="image/webp"&gt;\n  &lt;img src="fallback.jpg" alt="Пейзаж"&gt;\n&lt;/picture&gt;\n</code></pre><h3>Объяснение</h3><ol><li><code>srcset</code>: Разные размеры изображений.</li><li><code>&lt;picture&gt;</code>: Выбор формата.</li></ol><p>Оптимизируйте с TinyPNG.</p>',
                        topic_id=responsive_topic.id
                    ),
                    Lesson(
                        title='Мобильная оптимизация',
                        description='Улучшайте мобильный опыт пользователей.',
                        content='<p>Мобильная оптимизация улучшает UX на смартфонах.</p><ul><li><strong>Шрифты</strong>: Минимум 16px.</li><li><strong>Кнопки</strong>: Большие и кликабельные.</li></ul><h3>Пример кода</h3><pre><code>&lt;meta name="viewport" content="width=device-width, initial-scale=1.0"&gt;\n&lt;style&gt;\n  button {\n    padding: 15px;\n    font-size: 18px;\n  }\n  @media (max-width: 600px) {\n    nav {\n      flex-direction: column;\n    }\n  }\n&lt;/style&gt;\n</code></pre><h3>Объяснение</h3><ol><li><code>viewport</code>: Адаптивность.</li><li><code>flex-direction</code>: Мобильная навигация.</li></ol><p>Тестируйте с Lighthouse.</p>',
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
                        description='Познакомьтесь с JavaScript и его ролью.',
                        content='<p>JavaScript добавляет интерактивность веб-страницам: от анимаций до обработки форм.</p><ul><li><strong>Выполнение</strong>: В браузере через DOM.</li><li><strong>Подключение</strong>: Через <code>&lt;script&gt;</code>.</li></ul><h3>Пример кода</h3><pre><code>&lt;script&gt;\n  console.log("Привет, мир!");\n  document.querySelector("h1").textContent = "Новый заголовок";\n&lt;/script&gt;\n&lt;h1&gt;Заголовок&lt;/h1&gt;\n</code></pre><h3>Объяснение</h3><ol><li><code>console.log</code>: Вывод в консоль.</li><li><code>querySelector</code>: Выбор элемента.</li></ol><p>Тестируйте в DevTools (Console).</p>',
                        topic_id=js_topic.id
                    ),
                    Lesson(
                        title='Переменные и типы данных',
                        description='Работайте с переменными и типами данных.',
                        content='<p>Переменные хранят данные, а типы определяют их природу.</p><ul><li><strong>Переменные</strong>: <code>let</code>, <code>const</code>.</li><li><strong>Типы</strong>: Строки, числа, массивы.</li></ul><h3>Пример кода</h3><pre><code>let name = "Антон";\nconst age = 25;\nlet scores = [90, 85];\nconsole.log(typeof name);\n</code></pre><h3>Объяснение</h3><ol><li><code>let</code>: Переменная с изменяемым значением.</li><li><code>const</code>: Константа.</li><li><code>typeof</code>: Проверка типа.</li></ol><p>Используйте camelCase.</p>',
                        topic_id=js_topic.id
                    ),
                    Lesson(
                        title='Функции',
                        description='Создавайте и используйте функции.',
                        content='<p>Функции выполняют повторяющиеся задачи.</p><ul><li><strong>Объявление</strong>: <code>function</code> или <code>=&gt;</code>.</li><li><strong>Параметры</strong>: Передача данных.</li></ul><h3>Пример кода</h3><pre><code>function greet(name = "Гость") {\n  return `Привет, ${name}!`;\n}\nconsole.log(greet("Антон"));\n</code></pre><h3>Объяснение</h3><ol><li><code>function</code>: Определяет функцию.</li><li><code>return</code>: Возвращает результат.</li></ol><p>Тестируйте в Console.</p>',
                        topic_id=js_topic.id
                    ),
                    Lesson(
                        title='События',
                        description='Обрабатывайте события для интерактивности.',
                        content='<p>События, такие как клики, делают страницы интерактивными.</p><ul><li><strong>Слушатели</strong>: <code>addEventListener</code>.</li><li><strong>События</strong>: <code>click</code>, <code>input</code>.</li></ul><h3>Пример кода</h3><pre><code>&lt;button id="btn"&gt;Кликни&lt;/button&gt;\n&lt;script&gt;\n  document.querySelector("#btn").addEventListener("click", () => alert("Нажато!"));\n&lt;/script&gt;\n</code></pre><h3>Объяснение</h3><ol><li><code>addEventListener</code>: Слушает событие.</li><li><code>alert</code>: Всплывающее окно.</li></ol><p>Проверяйте в DevTools.</p>',
                        topic_id=js_topic.id
                    ),
                    Lesson(
                        title='Работа с DOM',
                        description='Манипулируйте элементами страницы.',
                        content='<p>DOM позволяет изменять HTML-структуру динамически.</p><ul><li><strong>Выбор</strong>: <code>querySelector</code>.</li><li><strong>Манипуляции</strong>: <code>innerHTML</code>, <code>createElement</code>.</li></ul><h3>Пример кода</h3><pre><code>&lt;div id="container"&gt;&lt;/div&gt;\n&lt;script&gt;\n  let div = document.querySelector("#container");\n  div.innerHTML = "&lt;p&gt;Текст&lt;/p&gt;";\n&lt;/script&gt;\n</code></pre><h3>Объяснение</h3><ol><li><code>querySelector</code>: Выбор элемента.</li><li><code>innerHTML</code>: Изменение содержимого.</li></ol><p>Оптимизируйте манипуляции для скорости.</p>',
                        topic_id=js_topic.id
                    ),
                ]
                db.session.add_all(js_lessons)
                print("Уроки для JavaScript добавлены:", len(js_lessons))

            # Наполнение уроков для Python
            if python_topic and not Lesson.query.filter_by(topic_id=python_topic.id).first():
                python_lessons = [
                    Lesson(
                        title='Введение в Python',
                        description='Познакомьтесь с Python и его возможностями.',
                        content='<p>Python — мощный язык с простым синтаксисом, популярный в веб-разработке и анализе данных.</p><ul><li><strong>Синтаксис</strong>: Читаемый и минималистичный.</li><li><strong>Применение</strong>: Веб, ML, автоматизация.</li></ul><h3>Пример кода</h3><pre><code>print("Привет, мир!")\nname = input("Имя: ")\nprint(f"Привет, {name}!")\n</code></pre><h3>Объяснение</h3><ol><li><code>print</code>: Вывод текста.</li><li><code>input</code>: Ввод данных.</li><li><code>f</code>: Форматирование строки.</li></ol><p>Тестируйте в терминале и следуйте PEP 8.</p>',
                        topic_id=python_topic.id
                    ),
                    Lesson(
                        title='Переменные и типы данных',
                        description='Работайте с переменными и типами данных.',
                        content='<p>Переменные в Python хранят данные разных типов.</p><ul><li><strong>Типы</strong>: <code>str</code>, <code>int</code>, <code>list</code>.</li><li><strong>Динамическая типизация</strong>: Тип определяется автоматически.</li></ul><h3>Пример кода</h3><pre><code>name = "Антон"\nage = 25\nscores = [90, 85]\nprint(type(name))\n</code></pre><h3>Объяснение</h3><ol><li><code>=</code>: Присваивание.</li><li><code>type</code>: Проверка типа.</li></ol><p>Используйте snake_case.</p>',
                        topic_id=python_topic.id
                    ),
                    Lesson(
                        title='Условные операторы',
                        description='Используйте if, elif, else для логики.',
                        content='<p>Условные операторы управляют выполнением кода.</p><ul><li><strong>Синтаксис</strong>: <code>if</code>, <code>elif</code>, <code>else</code>.</li><li><strong>Отступы</strong>: 4 пробела.</li></ul><h3>Пример кода</h3><pre><code>age = 18\nif age >= 18:\n    print("Взрослый")\nelse:\n    print("Ребенок")\n</code></pre><h3>Объяснение</h3><ol><li><code>if</code>: Условие.</li><li><code>else</code>: Альтернатива.</li></ol><p>Тестируйте в терминале.</p>',
                        topic_id=python_topic.id
                    ),
                    Lesson(
                        title='Циклы',
                        description='Освойте for и while для повторений.',
                        content='<p>Циклы автоматизируют повторяющиеся задачи.</p><ul><li><strong>for</strong>: Для итерируемых объектов.</li><li><strong>while</strong>: По условию.</li></ul><h3>Пример кода</h3><pre><code>for i in range(3):\n    print(i)\ncount = 0\nwhile count < 3:\n    print(count)\n    count += 1\n</code></pre><h3>Объяснение</h3><ol><li><code>range</code>: Генерирует числа.</li><li><code>while</code>: Повторяет по условию.</li></ol><p>Избегайте бесконечных циклов.</p>',
                        topic_id=python_topic.id
                    ),
                    Lesson(
                        title='Функции',
                        description='Создавайте функции для модульности.',
                        content='<p>Функции группируют код для повторного использования.</p><ul><li><strong>Объявление</strong>: <code>def</code>.</li><li><strong>Параметры</strong>: Передача данных.</li></ul><h3>Пример кода</h3><pre><code>def greet(name="Гость"):\n    return f"Привет, {name}!"\nprint(greet("Антон"))\n</code></pre><h3>Объяснение</h3><ol><li><code>def</code>: Определяет функцию.</li><li><code>return</code>: Возвращает результат.</li></ol><p>Документируйте с docstring.</p>',
                        topic_id=python_topic.id
                    ),
                ]
                db.session.add_all(python_lessons)
                print("Уроки для Python добавлены:", len(python_lessons))

            db.session.commit()
            print("База данных успешно наполнена.")

if __name__ == '__main__':
    update_lessons()