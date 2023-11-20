document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const references = document.querySelectorAll('.single-publication');
    const searchResults = document.getElementById('search-results');
    const clearButton = document.getElementById('clear-btn');
    const addToCart = document.querySelector('.default-btn')
    
    let originalReferences = Array.from(references); // Guardar el orden original de los elementos
    
    clearButton.addEventListener('click', function () {
        window.location.reload(); // Recargar la página
    });

    searchInput.addEventListener('input', function () {
        const searchTerm = this.value.trim().toLowerCase();
        searchResults.innerHTML = ''; // Limpiar los resultados anteriores
        let found = false;

        references.forEach(reference => {
            const referenceName = reference.querySelector('h3 a').textContent.toLowerCase();

            if (referenceName.includes(searchTerm)) {
                found = true;
                searchResults.appendChild(reference);
            } else {
                reference.style.display = 'none'; // Ocultar elementos que no 
            }
        });

        if (searchTerm === '') {
            references.forEach(reference => {
                reference.style.display = 'block'; // Mostrar todos los elementos si no hay término de búsqueda
            });
        }
    });
});
