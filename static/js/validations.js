console.log("Validations script loaded.");
const form = document.querySelector("form");
const nombreInput = document.getElementById("nombre");
const nombreTag = document.getElementById("name_tag");
const passwordInput = document.getElementById("password");

// Crear un contenedor para mostrar mensajes de error de la contraseña
const passwordTag = document.createElement("small");
passwordTag.className = "text-danger";
passwordInput.parentNode.appendChild(passwordTag);

// Función para validar el nombre completo
function validarNombre() {
    const nombre = nombreInput.value.trim();
    const nombreRegex = /^[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(\s[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+$/;

    if (!nombreRegex.test(nombre)) {
        nombreTag.style.color = "red";
        nombreTag.textContent = "Por favor, ingrese un nombre completo válido. Ejemplo: 'Juan Pérez' o 'María López'.";
        return false;
    } else {
        nombreTag.style.color = "black";
        nombreTag.textContent = "";
        return true;
    }
}

// Función para validar la contraseña
function validarPassword() {
    const password = passwordInput.value.trim();
    const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

    if (!passwordRegex.test(password)) {
        passwordTag.textContent = "La contraseña debe tener al menos 8 caracteres, incluir una mayúscula, un número y un carácter especial.";
        return false;
    } else {
        passwordTag.textContent = "";
        return true;
    }
}

// Validar el nombre completo al perder el foco
nombreInput.addEventListener("blur", validarNombre);

// Validar la contraseña al perder el foco
passwordInput.addEventListener("blur", validarPassword);

// Validar todo el formulario antes de enviarlo
form.addEventListener("submit", function (event) {
    const esNombreValido = validarNombre();
    const esPasswordValido = validarPassword();

    if (!esNombreValido || !esPasswordValido) {
        event.preventDefault(); // Evitar el envío del formulario si alguna validación falla
        alert("Por favor, corrija los errores antes de enviar el formulario.");
    }
});

