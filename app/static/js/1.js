// Este código crea un temporizador que espera 2 segundos y luego selecciona un elemento en el documento 
// con la clase "msg"
setTimeout(function(){
    elementoP = document.querySelector('.msg');
    elementoP.style.display = 'none';

    // Después de ocultar el elemento, muestra una notificación de éxito con SweetAlert2
    Swal.fire({
        position: 'top-end',
        icon: 'success',
        title: 'Your work has been saved',
        showConfirmButton: false,
        timer: 1500
    });
}, 2000);
