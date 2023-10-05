document.addEventListener("DOMContentLoaded", function () {
    // Obtener la parte de la URL que contiene el identificador de la imagen
    const imageId = window.location.pathname.split("/").pop();

    // Crear la URL completa de la imagen
    const imageUrl = "{{ url_for('static', filename='img/') }}" + imageId;

    // Actualizar la fuente de la imagen en el elemento img
    let selectedImage = document.getElementById("selected-image");
    selectedImage.src = imageUrl;
});