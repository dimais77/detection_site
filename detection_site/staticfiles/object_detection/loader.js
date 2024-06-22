// После загрузки страницы выполняется этот скрипт
document.addEventListener("DOMContentLoaded", function() {
    const forms = document.querySelectorAll('.process-form');

    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            const button = form.querySelector('.process-button');
            const loader = form.querySelector('.loader');

            // Показать индикатор загрузки
            loader.style.display = 'block';

            // Отключить кнопку отправки, чтобы предотвратить множественные отправки
            button.disabled = true;
        });
    });
});
