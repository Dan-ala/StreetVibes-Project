// Estructura de datos con las URLs de cada categoría
const categoryUrls = {
    1: '',
    2: 'http://localhost/PROYECTO_PERSONALIZACION_ARTICULOS/referencia/busosOver.php',
    3: 'http://localhost/PROYECTO_PERSONALIZACION_ARTICULOS/referencia/categoria3.php',
    4: 'http://localhost/PROYECTO_PERSONALIZACION_ARTICULOS/referencia/categoria4.php',
    // Añade más categorías y sus URLs aquí según sea necesario
  };
  
  // Obtén todos los botones de categoría por su clase
  let buttons = document.querySelectorAll('.btn-primary');
  
  // Agrega un event listener a cada botón
  buttons.forEach(button => {
    button.addEventListener('click', () => {
      // Obtén el ID de la categoría del botón actual
      let idCate = button.id;
  
      // Verifica si la categoría tiene una URL asociada
      if (categoryUrls.hasOwnProperty(idCate)) {
        // Obtiene la URL correspondiente a la categoría
        let categoryUrl = categoryUrls[idCate];
        
        // Redirecciona a la URL correspondiente a la categoría
        window.location.href = categoryUrl;
      } else {
        // Manejar el caso en el que no haya una URL definida para la categoría
        console.log('No se encontró una URL para la categoría seleccionada');
      }
    });
  });
  