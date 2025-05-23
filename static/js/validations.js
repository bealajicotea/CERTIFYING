console.log("Validations script loaded.");
const form = document.querySelector("form");
const nombreInput = document.getElementById("id-first_name");
const nombreTag = document.getElementById("name_tag");
const passwordInput = document.getElementById("id-password");
const emailInput = document.getElementById("id-email");
const usernameInput = document.getElementById("id-username");

// Mensaje de error para contraseña
const passwordTag = document.createElement("small");
passwordTag.className = "text-danger";
passwordInput.parentNode.appendChild(passwordTag);

// Mensaje de error para correo
const emailTag = document.createElement("small");
emailTag.className = "text-danger";
emailInput.parentNode.appendChild(emailTag);

// Validar nombre y apellido (ambos con mayúscula inicial y al menos un apellido)
function validarNombre() {
    const nombre = nombreInput.value.trim();
    // Debe tener al menos dos palabras, ambas con mayúscula inicial y minúsculas después
    const nombreRegex = /^([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)(\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*$/;

    if (!nombre) {
        nombreTag.style.color = "red";
        nombreTag.textContent = "El campo nombre no puede estar vacío.";
        return false;
    } else if (!nombreRegex.test(nombre)) {
        nombreTag.style.color = "red";
        nombreTag.textContent = "Ingrese nombre y al menos un apellido, ambos con mayúscula inicial.";
        return false;
    } else {
        nombreTag.style.color = "black";
        nombreTag.textContent = "";
        return true;
    }
}

// Validar contraseña: mínimo 8 caracteres, una mayúscula y un carácter especial
function validarPassword() {
    const password = passwordInput.value.trim();
    const passwordRegex = /^(?=.*[A-Z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

    if (!passwordRegex.test(password)) {
        passwordTag.textContent = "La contraseña debe tener al menos 8 caracteres, una mayúscula y un carácter especial.";
        return false;
    } else {
        passwordTag.textContent = "";
        return true;
    }
}

// Validar correo UCI y que el usuario antes del @ sea igual al username
function validarEmail() {
    const email = emailInput.value.trim();
    const username = usernameInput.value.trim();
    const emailRegex = /^[\w\.-]+@uci\.cu$/i;

    if (!emailRegex.test(email)) {
        emailTag.textContent = "El correo debe terminar en @uci.cu";
        return false;
    }
    const emailUser = email.split('@')[0];
    if (emailUser !== username) {
        emailTag.textContent = "El correo debe comenzar con el mismo usuario que el username.";
        return false;
    }
    emailTag.textContent = "";
    return true;
}

// Eventos de validación
nombreInput.addEventListener("blur", validarNombre);
passwordInput.addEventListener("blur", validarPassword);
emailInput.addEventListener("blur", validarEmail);

form.addEventListener("submit", function (event) {
    const esNombreValido = validarNombre();
    const esPasswordValido = validarPassword();
    const esEmailValido = validarEmail();

    if (!esNombreValido || !esPasswordValido || !esEmailValido) {
        event.preventDefault();
        alert("Por favor, corrija los errores antes de enviar el formulario.");
    }
});

