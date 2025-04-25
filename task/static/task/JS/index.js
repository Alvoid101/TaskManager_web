// Código existente para la búsqueda
let searchBox = document.getElementById("ShearchBox")
let searchButton = document.getElementById("shearchButton")

function clickSearchButton(){
    let value = searchBox.value
    searchButton.href = "https://www.google.com/search?q=" + value
}

searchButton.addEventListener("click", clickSearchButton)

// Funcionalidad para el modal de categorías
document.addEventListener('DOMContentLoaded', function() {
    // Obtener referencias a los elementos del modal
    const categoryModal = document.getElementById("categoryModal");
    const addCategoryBtn = document.getElementById("addCategoryBtn");
    const closeBtn = document.querySelector("#categoryModal .close");
    
    // Comprobar si existen los elementos antes de añadir event listeners
    if (addCategoryBtn) {
        // Abrir el modal cuando se hace clic en el botón
        addCategoryBtn.addEventListener('click', function() {
            if (categoryModal) {
                categoryModal.style.display = "block";
                console.log("Modal abierto");
            }
        });
    }
    
    // Cerrar el modal cuando se hace clic en la X
    if (closeBtn && categoryModal) {
        closeBtn.addEventListener('click', function() {
            categoryModal.style.display = "none";
        });
    }
    
    // Cerrar el modal cuando se hace clic fuera de él
    if (categoryModal) {
        window.addEventListener('click', function(event) {
            if (event.target === categoryModal) {
                categoryModal.style.display = "none";
            }
        });
    }
});