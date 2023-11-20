document.addEventListener('DOMContentLoaded', function () {
    let cart = document.querySelector('.cart');
    let btnOpen = document.querySelector('#openModal')
    let closeModal = document.querySelector('#closeModal')

    btnOpen.addEventListener("click", (e) => {
        e.preventDefault();
        cart.classList.add("active");
    });

    // Close cart
    closeModal.addEventListener("click", () => {
        cart.classList.remove("active");
    });
});
