document.addEventListener('DOMContentLoaded', function() {
    const filterDropdowns = document.querySelectorAll('.admin-filter-dropdown');

    filterDropdowns.forEach(dropdown => {
        const links = dropdown.querySelectorAll('a');

        links.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();

                // Удаляем класс selected у всех ссылок
                links.forEach(l => l.parentElement.classList.remove('selected'));

                // Добавляем класс selected к выбранной ссылке
                this.parentElement.classList.add('selected');

                // Переходим по ссылке
                window.location.href = this.href;
            });
        });
    });
});