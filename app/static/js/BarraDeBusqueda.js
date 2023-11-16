  // Agregar JavaScript para filtrar las referencias en tiempo real
  document.getElementById('search-input').addEventListener('input', function () {
    const searchTerm = this.value.toLowerCase();
    const references = document.querySelectorAll('.single-publication');

    references.forEach(reference => {
        const referenceName = reference.querySelector('h3 a').textContent.toLowerCase();

        if (referenceName.includes(searchTerm)) {
            reference.style.display = 'block';
        } else {
            reference.style.display = 'none';
        }
    });
});