
// Obtener el año actual
const currentYear = new Date().getFullYear();
// Asignar el año al elemento con id "current-year"
document.getElementById('current-year').textContent = currentYear;

// Configurar el observador de intersección para las animaciones de fade-in
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, {
    threshold: 0.1
});

document.querySelectorAll('.fade-in-section').forEach(section => {
    observer.observe(section);
});

feather.replace();

// Función para abrir el modal
function openModal(element) {
    var modal = document.getElementById("imageModal");
    var modalImg = document.getElementById("modalImg");
    var closeBtn = document.querySelector(".close");
    
    modal.style.display = "flex";
    modal.style.justifyContent = "center"; // Centrar horizontalmente
    modal.style.alignItems = "center"; // Centrar verticalmente
    
    modalImg.src = element.parentElement.parentElement.querySelector(".gallery-image").src;
    modalImg.style.maxWidth = "70%";  // Ajusta el tamaño máximo de la imagen
    modalImg.style.maxHeight = "70%"; // Ajusta la altura máxima de la imagen
    modalImg.style.borderRadius = "10px";
    modalImg.style.objectFit = "contain";
    modalImg.style.cursor = "pointer"; // Cambiar el cursor a pointer
    
    closeBtn.style.position = "absolute";
    closeBtn.style.top = "20px";
    closeBtn.style.right = "30px";
    closeBtn.style.color = "white";
    closeBtn.style.fontSize = "40px";
    closeBtn.style.cursor = "pointer";
}

// Función para cerrar el modal
function closeModal() {
    document.getElementById("imageModal").style.display = "none";
}
