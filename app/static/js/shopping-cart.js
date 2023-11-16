// Cart
let cartIcon = document.querySelector("#cart-icon");
let cart = document.querySelector(".cart");
let closeCart = document.querySelector("#close-cart");

cartIcon.addEventListener("click", () => {
    cart.classList.add("active");
});

// Close cart
closeCart.addEventListener("click", () => {
    cart.classList.remove("active");
});

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", ready);
} else {
    ready();
}

function ready() {
    let removeCartButton = document.getElementsByClassName('cart-remove');
    for (let i = 0; i < removeCartButton.length; i++) {
        let button = removeCartButton[i];
        button.addEventListener('click', removeCartItem);
    }

    let quantityInputs = document.getElementsByClassName("cart-quantity");
    for (let i = 0; i < quantityInputs.length; i++) { // Add .length here
        let input = quantityInputs[i];
        input.addEventListener("change", quantityChanged);
    }
}

function removeCartItem(event) {
    let buttonClicked = event.target;
    buttonClicked.parentElement.parentElement.remove(); // Adjust the DOM traversal
    updateTotal();
}

function quantityChanged(event) {
    let input = event.target;
    if (isNaN(input.value) || input.value <= 0) {
        input.value = 1;
    }
    updateTotal();
}


// Variable para almacenar los productos en el carrito
const cartProducts = [];

// Función para manejar el clic en el ícono 🚗
function addCartClicked(idRef) {
  // Busca el producto correspondiente en tus datos (referencias)
  const product = referencias.find((referencia) => referencia['idRef'] === idRef);

  // Agrega el producto al carrito
  cartProducts.push(product);

  // Llama a una función para mostrar el producto en el carrito
  displayProductInCart(product);

  // También puedes actualizar el precio total y otros detalles aquí
}

// Función para mostrar un producto en el carrito
function displayProductInCart(product) {
  // Crea un nuevo elemento de carrito para mostrar el producto
  const cartItem = document.createElement("div");
  cartItem.classList.add("cart-item");
  
  // Construye el contenido del elemento de carrito (similar a lo que hiciste en el bucle anterior)
  // Puedes usar product['nomRef'], product['precioRef'], etc.

  // Agrega el elemento de carrito al carrito
  const cartItems = document.querySelector(".cart-items");
  cartItems.appendChild(cartItem);
}

// Otras funciones para actualizar el precio total y eliminar productos del carrito


// Update Total
function updateTotal() {
    let cartContent = document.querySelector(".cart-content"); // Use querySelector
    let cartBoxes = cartContent.getElementsByClassName("cart-box"); // Use cart-box, not cart-price
    let total = 0; // Initialize total

    for (let i = 0; i < cartBoxes.length; i++) {
        let cartBox = cartBoxes[i];
        let priceElement = cartBox.getElementsByClassName("cart-price")[0];
        let quantityElement = cartBox.getElementsByClassName("cart-quantity")[0];
        let price = parseFloat(priceElement.innerText.replace('$', ''));
        let quantity = quantityElement.value;
        total += price * quantity;
    }

    document.querySelector(".total-price").innerText = "$" + total;
}