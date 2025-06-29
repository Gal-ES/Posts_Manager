document.addEventListener('DOMContentLoaded', function() {
    // Получаем поисковый запрос из URL
    const urlParams = new URLSearchParams(window.location.search);
    const searchQuery = urlParams.get('q');
    if (!searchQuery) return;

    // Находим индекс столбца 'Заголовок'
    const ths = document.querySelectorAll('.model-post th');
    let titleColIdx = -1;
    ths.forEach((th, idx) => {
        if (th.textContent.trim().toLowerCase().includes('заголовок')) {
            titleColIdx = idx;
        }
    });
    if (titleColIdx === -1) return;

    // Подсвечиваем только в ячейках столбца 'Заголовок'
    const rows = document.querySelectorAll('.model-post tbody tr');
    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        if (cells.length > titleColIdx) {
            const cell = cells[titleColIdx];
            const text = cell.textContent;
            if (text.toLowerCase().includes(searchQuery.toLowerCase())) {
                const regex = new RegExp(searchQuery, 'gi');
                cell.innerHTML = text.replace(regex, match => `<span class="search-highlight">${match}</span>`);
            }
        }
    });
});