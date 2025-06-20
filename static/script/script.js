document.addEventListener("DOMContentLoaded", function () {
    const themeToggleButton = document.getElementById('theme-toggle');
    const themes = ['dark-mode', 'light-mode', 'light-alt-mode', 'orange-mode'];

    if (themeToggleButton) {
        themeToggleButton.addEventListener('click', function () {
            let currentTheme = themes.find(theme => document.body.classList.contains(theme)) || 'light-mode';
            let currentIndex = themes.indexOf(currentTheme);
            let nextIndex = (currentIndex + 1) % themes.length;
            let nextTheme = themes[nextIndex];

            console.log(`Переключение с ${currentTheme} на ${nextTheme}`); // Для отладки

            themes.forEach(theme => document.body.classList.remove(theme));
            document.body.classList.add(nextTheme);
            localStorage.setItem('theme', nextTheme);
        });
    } else {
        console.error('Кнопка с id="theme-toggle" не найдена');
    }

    const savedTheme = localStorage.getItem('theme');
    if (savedTheme && themes.includes(savedTheme)) {
        console.log(`Применяется сохранённая тема: ${savedTheme}`); // Для отладки
        document.body.classList.add(savedTheme);
    } else {
        console.log('Применяется тема по умолчанию: light-mode'); // Для отладки
        document.body.classList.add('light-mode');
        localStorage.setItem('theme', 'light-mode');
    }
});