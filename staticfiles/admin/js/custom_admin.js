document.addEventListener('DOMContentLoaded', function() {
    // Находим все кнопки "Вернуться без сохранения"
    const cancelButtons = document.querySelectorAll('input[value="Вернуться без сохранения"]');

    cancelButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();

            // Проверяем, были ли изменения в форме
            const form = document.querySelector('form#post_form');
            if (form && form.dataset.changed === 'true') {
                if (confirm('Вы уверены, что хотите вернуться без сохранения изменений?')) {
                    window.location.href = this.getAttribute('onclick').match(/'([^']+)'/)[1];
                }
            } else {
                window.location.href = this.getAttribute('onclick').match(/'([^']+)'/)[1];
            }
        });
    });

    // Отслеживаем изменения в форме
    const form = document.querySelector('form#post_form');
    if (form) {
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('change', function() {
                form.dataset.changed = 'true';
            });
        });
    }
});