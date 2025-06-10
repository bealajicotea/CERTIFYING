document.addEventListener('DOMContentLoaded', function() {
    console.log("Validación de usuario iniciada");
    const usernameInput = document.getElementById('id-username');
    const usernameError = document.getElementById('username-error');
    if (usernameInput && usernameError) {
        usernameInput.addEventListener('input', function() {
            const value = usernameInput.value;
            if (!value) {
                usernameError.textContent = "El usuario es obligatorio.";
                usernameError.style.display = "block";
                usernameInput.classList.add('is-invalid');
            } else if (!/^[a-z]+$/.test(value)) {
                usernameError.textContent = "El usuario solo puede contener letras minúsculas (a-z).";
                usernameError.style.display = "block";
                usernameInput.classList.add('is-invalid');
            } else {
                usernameError.textContent = "";
                usernameError.style.display = "none";
                usernameInput.classList.remove('is-invalid');
            }
        });
    }

    // Password: min 6 chars, at least 1 lowercase, 1 uppercase, 1 number, 1 special char
    const passwordInput = document.getElementById('id-password');
    let passwordError = document.getElementById('password-error');
    if (passwordInput) {
        if (!passwordError) {
            passwordError = document.createElement('div');
            passwordError.id = 'password-error';
            passwordError.style = "color: #dc3545; font-size: 0.95em; margin-top: 0.25rem; display: none;";
            passwordInput.parentNode.appendChild(passwordError);
        }
        passwordInput.addEventListener('input', function() {
            const value = passwordInput.value;
            const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d]).{6,}$/;
            if (!value) {
                passwordError.textContent = "La contraseña es obligatoria.";
                passwordError.style.display = "block";
                passwordInput.classList.add('is-invalid');
            } else if (!regex.test(value)) {
                passwordError.textContent = "La contraseña debe tener al menos 6 caracteres, incluir mayúsculas, minúsculas, números y caracteres especiales.";
                passwordError.style.display = "block";
                passwordInput.classList.add('is-invalid');
            } else {
                passwordError.textContent = "";
                passwordError.style.display = "none";
                passwordInput.classList.remove('is-invalid');
            }
        });
    }

    // Email
    const emailInput = document.getElementById('id-email');
    let emailError = document.getElementById('email-error');
    if (emailInput) {
        if (!emailError) {
            emailError = document.createElement('div');
            emailError.id = 'email-error';
            emailError.style = "color: #dc3545; font-size: 0.95em; margin-top: 0.25rem; display: none;";
            emailInput.parentNode.appendChild(emailError);
        }
        emailInput.addEventListener('input', function() {
            const value = emailInput.value;
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!value) {
                emailError.textContent = "El correo electrónico es obligatorio.";
                emailError.style.display = "block";
                emailInput.classList.add('is-invalid');
            } else if (!emailRegex.test(value)) {
                emailError.textContent = "Ingrese un correo electrónico válido.";
                emailError.style.display = "block";
                emailInput.classList.add('is-invalid');
            } else {
                emailError.textContent = "";
                emailError.style.display = "none";
                emailInput.classList.remove('is-invalid');
            }
        });
    }

    // First Name: must start with uppercase, only letters and spaces, not empty
    const firstNameInput = document.getElementById('id-first_name');
    let firstNameError = document.getElementById('first_name-error');
    if (firstNameInput) {
        if (!firstNameError) {
            firstNameError = document.createElement('div');
            firstNameError.id = 'first_name-error';
            firstNameError.style = "color: #dc3545; font-size: 0.95em; margin-top: 0.25rem; display: none;";
            firstNameInput.parentNode.appendChild(firstNameError);
        }
        firstNameInput.addEventListener('input', function() {
            const value = firstNameInput.value;
            const regex = /^[A-ZÁÉÍÓÚÑ][a-záéíóúñA-ZÁÉÍÓÚÑ\s]*$/;
            if (!value) {
                firstNameError.textContent = "El nombre es obligatorio.";
                firstNameError.style.display = "block";
                firstNameInput.classList.add('is-invalid');
            } else if (!regex.test(value)) {
                firstNameError.textContent = "El nombre debe empezar con mayúscula y solo contener letras.";
                firstNameError.style.display = "block";
                firstNameInput.classList.add('is-invalid');
            } else {
                firstNameError.textContent = "";
                firstNameError.style.display = "none";
                firstNameInput.classList.remove('is-invalid');
            }
        });
    }

    // Last Name: must start with uppercase, only letters and spaces, not empty
    const lastNameInput = document.getElementById('id-last_name');
    let lastNameError = document.getElementById('last_name-error');
    if (lastNameInput) {
        if (!lastNameError) {
            lastNameError = document.createElement('div');
            lastNameError.id = 'last_name-error';
            lastNameError.style = "color: #dc3545; font-size: 0.95em; margin-top: 0.25rem; display: none;";
            lastNameInput.parentNode.appendChild(lastNameError);
        }
        lastNameInput.addEventListener('input', function() {
            const value = lastNameInput.value;
            const regex = /^[A-ZÁÉÍÓÚÑ][a-záéíóúñA-ZÁÉÍÓÚÑ\s]*$/;
            if (!value) {
                lastNameError.textContent = "El apellido es obligatorio.";
                lastNameError.style.display = "block";
                lastNameInput.classList.add('is-invalid');
            } else if (!regex.test(value)) {
                lastNameError.textContent = "El apellido debe empezar con mayúscula y solo contener letras.";
                lastNameError.style.display = "block";
                lastNameInput.classList.add('is-invalid');
            } else {
                lastNameError.textContent = "";
                lastNameError.style.display = "none";
                lastNameInput.classList.remove('is-invalid');
            }
        });
    }
});
