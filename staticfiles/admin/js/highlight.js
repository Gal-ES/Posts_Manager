document.addEventListener('DOMContentLoaded', function() {
    // Получаем поисковый запрос из URL
    const urlParams = new URLSearchParams(window.location.search);
    const searchQuery = urlParams.get('q');

    if (searchQuery) {
        // Находим все ячейки таблицы
        const cells = document.querySelectorAll('td');

        cells.forEach(cell => {
            const text = cell.textContent;
            if (text.toLowerCase().includes(searchQuery.toLowerCase())) {
                // Заменяем найденный текст на подсвеченный
                const regex = new RegExp(searchQuery, 'gi');
                cell.innerHTML = text.replace(regex, match =>
                    `<span class="search-highlight">${match}</span>`
                );
            }
        });
    }
});