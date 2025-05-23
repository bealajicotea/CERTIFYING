console.log("Validations script loaded.");
const form = document.querySelector("form");
const first_nameInput = document.getElementById("id-first_name");
const first_nameTag = document.getElementById("id-first_name");
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

// Validar first name: debe comenzar con mayúscula
function validarFirst_name() {
    const first_name = first_nameInput.value.trim();
    const first_nameRegex = /^[A-ZÁÉÍÓÚÑ][a-záéíóúñ]*/;

    if (!first_name) {
        first_nameTag.style.color = "red";
        first_nameTag.textContent = "El campo nombre no puede estar vacío.";
        return false;
    } else if (!first_nameRegex.test(first_name)) {
        first_nameTag.style.color = "red";
        first_nameTag.textContent = "El nombre debe comenzar con mayúscula.";
        return false;
    } else {
        first_nameTag.style.color = "black";
        first_nameTag.textContent = "";
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
first_nameInput.addEventListener("blur", validarFirst_name);
passwordInput.addEventListener("blur", validarPassword);
emailInput.addEventListener("blur", validarEmail);

form.addEventListener("submit", function (event) {
    const esFirstNameValido = validarFirst_name();
    const esPasswordValido = validarPassword();
    const esEmailValido = validarEmail();

    if (!esFirstNameValido || !esPasswordValido || !esEmailValido) {
        event.preventDefault();
        alert("Por favor, corrija los errores antes de enviar el formulario.");
    }
});

