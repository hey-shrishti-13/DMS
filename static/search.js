document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.querySelector(".search-input");
    const categorySelect = document.querySelector(".search-select");
    const tableRows = document.querySelectorAll("tbody tr");

    function filterTable() {
        const searchValue = searchInput.value.toLowerCase().trim();
        const categoryValue = categorySelect.value;

        tableRows.forEach(row => {
            const filename = row.querySelector("td[data-label='Filename']")?.textContent.toLowerCase() || "";
            const type = row.querySelector("td[data-label='Type'], td[data-label='Document Type']")?.textContent || "";

            const matchesSearch = filename.includes(searchValue);
            const matchesCategory = categoryValue === "all" || type === categoryValue;

            if (matchesSearch && matchesCategory) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    }

    searchInput?.addEventListener("input", filterTable);
    categorySelect?.addEventListener("change", filterTable);
});
