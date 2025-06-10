document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('usuario-form');
    if (!form) return;

    // Referencias a los campos y errores
    const usernameInput = document.getElementById('id-username');
    const usernameError = document.getElementById('username-error');
    const passwordInput = document.getElementById('id-password');
    let passwordError = document.getElementById('password-error');
    const emailInput = document.getElementById('id-email');
    let emailError = document.getElementById('email-error');
    const firstNameInput = document.getElementById('id-first_name');
    let firstNameError = document.getElementById('first_name-error');
    const lastNameInput = document.getElementById('id-last_name');
    let lastNameError = document.getElementById('last_name-error');
    const tipoUsuarioInput = document.getElementById('id-tipo_usuario');
    let tipoUsuarioError = document.getElementById('tipo_usuario-error');

    // Crear errores si no existen
    function ensureErrorDiv(input, errorDiv, id) {
        if (!input) return null;
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.id = id;
            errorDiv.style = "color: #dc3545; font-size: 0.95em; margin-top: 0.25rem; display: none;";
            input.parentNode.appendChild(errorDiv);
        }
        return errorDiv;
    }
    passwordError = ensureErrorDiv(passwordInput, passwordError, 'password-error');
    emailError = ensureErrorDiv(emailInput, emailError, 'email-error');
    firstNameError = ensureErrorDiv(firstNameInput, firstNameError, 'first_name-error');
    lastNameError = ensureErrorDiv(lastNameInput, lastNameError, 'last_name-error');
    tipoUsuarioError = ensureErrorDiv(tipoUsuarioInput, tipoUsuarioError, 'tipo_usuario-error');

    // Referencias a las tabs y contenidos de pestañas
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');

    form.addEventListener('submit', function(e) {
        let valid = true;
        let firstInvalid = null;
        let firstInvalidTabId = null;

        // Username
        if (usernameInput && usernameError) {
            const value = usernameInput.value;
            if (!value) {
                usernameError.textContent = "El usuario es obligatorio.";
                usernameError.style.display = "block";
                usernameInput.classList.add('is-invalid');
                valid = false;
                if (!firstInvalid) firstInvalid = usernameInput;
            } else if (!/^[a-z]+$/.test(value)) {
                usernameError.textContent = "El usuario solo puede contener letras minúsculas (a-z).";
                usernameError.style.display = "block";
                usernameInput.classList.add('is-invalid');
                valid = false;
                if (!firstInvalid) firstInvalid = usernameInput;
            } else {
                usernameError.textContent = "";
                usernameError.style.display = "none";
                usernameInput.classList.remove('is-invalid');
            }
        }

        // Password
        if (passwordInput && passwordError) {
            const value = passwordInput.value;
            const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d]).{6,}$/;
            if (!value) {
                passwordError.textContent = "La contraseña es obligatoria.";
                passwordError.style.display = "block";
                passwordInput.classList.add('is-invalid');
                valid = false;
                if (!firstInvalid) firstInvalid = passwordInput;
            } else if (!regex.test(value)) {
                passwordError.textContent = "La contraseña debe tener al menos 6 caracteres, incluir mayúsculas, minúsculas, números y caracteres especiales.";
                passwordError.style.display = "block";
                passwordInput.classList.add('is-invalid');
                valid = false;
                if (!firstInvalid) firstInvalid = passwordInput;
            } else {
                passwordError.textContent = "";
                passwordError.style.display = "none";
                passwordInput.classList.remove('is-invalid');
            }
        }

        // Email
        if (emailInput && emailError) {
            const value = emailInput.value;
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!value) {
                emailError.textContent = "El correo electrónico es obligatorio.";
                emailError.style.display = "block";
                emailInput.classList.add('is-invalid');
                valid = false;
                if (!firstInvalid) firstInvalid = emailInput;
            } else if (!emailRegex.test(value)) {
                emailError.textContent = "Ingrese un correo electrónico válido.";
                emailError.style.display = "block";
                emailInput.classList.add('is-invalid');
                valid = false;
                if (!firstInvalid) firstInvalid = emailInput;
            } else {
                emailError.textContent = "";
                emailError.style.display = "none";
                emailInput.classList.remove('is-invalid');
            }
        }

        // First Name
        if (firstNameInput && firstNameError) {
            const value = firstNameInput.value;
            const regex = /^[A-ZÁÉÍÓÚÑ][a-záéíóúñA-ZÁÉÍÓÚÑ\s]*$/;
            if (!value) {
                firstNameError.textContent = "El nombre es obligatorio.";
                firstNameError.style.display = "block";
                firstNameInput.classList.add('is-invalid');
                valid = false;
                if (!firstInvalid) firstInvalid = firstNameInput;
            } else if (!regex.test(value)) {
                firstNameError.textContent = "El nombre debe empezar con mayúscula y solo contener letras.";
                firstNameError.style.display = "block";
                firstNameInput.classList.add('is-invalid');
                valid = false;
                if (!firstInvalid) firstInvalid = firstNameInput;
            } else {
                firstNameError.textContent = "";
                firstNameError.style.display = "none";
                firstNameInput.classList.remove('is-invalid');
            }
        }

        // Last Name
        if (lastNameInput && lastNameError) {
            const value = lastNameInput.value;
            const regex = /^[A-ZÁÉÍÓÚÑ][a-záéíóúñA-ZÁÉÍÓÚÑ\s]*$/;
            if (!value) {
                lastNameError.textContent = "El apellido es obligatorio.";
                lastNameError.style.display = "block";
                lastNameInput.classList.add('is-invalid');
                valid = false;
                if (!firstInvalid) firstInvalid = lastNameInput;
            } else if (!regex.test(value)) {
                lastNameError.textContent = "El apellido debe empezar con mayúscula y solo contener letras.";
                lastNameError.style.display = "block";
                lastNameInput.classList.add('is-invalid');
                valid = false;
                if (!firstInvalid) firstInvalid = lastNameInput;
            } else {
                lastNameError.textContent = "";
                lastNameError.style.display = "none";
                lastNameInput.classList.remove('is-invalid');
            }
        }

        // Tipo de usuario obligatorio
        if (tipoUsuarioInput && tipoUsuarioError) {
            const value = tipoUsuarioInput.value;
            if (!value) {
                tipoUsuarioError.textContent = "El tipo de usuario es obligatorio.";
                tipoUsuarioError.style.display = "block";
                tipoUsuarioInput.classList.add('is-invalid');
                valid = false;
                if (!firstInvalid) firstInvalid = tipoUsuarioInput;
            } else {
                tipoUsuarioError.textContent = "";
                tipoUsuarioError.style.display = "none";
                tipoUsuarioInput.classList.remove('is-invalid');
            }
        }

        // Guardar el id de la pestaña donde está el primer campo inválido
        if (firstInvalid) {
            let parentTabContent = firstInvalid.closest('.tab-content');
            if (parentTabContent && parentTabContent.id) {
                firstInvalidTabId = parentTabContent.id;
            }
        }

        if (!valid) {
            e.preventDefault();
            // Cambiar a la pestaña correspondiente si es necesario
            if (firstInvalidTabId) {
                // Quitar active de todas las tabs y esconder tab contents
                tabs.forEach(t => {
                    t.classList.remove('active');
                    t.setAttribute('aria-selected', 'false');
                    t.setAttribute('tabindex', '-1');
                });
                tabContents.forEach(c => {
                    c.classList.remove('active');
                    c.hidden = true;
                });

                // Activar la tab y contenido correspondiente
                const tabToActivate = Array.from(tabs).find(tab => tab.dataset.tab === firstInvalidTabId);
                if (tabToActivate) {
                    tabToActivate.classList.add('active');
                    tabToActivate.setAttribute('aria-selected', 'true');
                    tabToActivate.setAttribute('tabindex', '0');
                }
                const contentToActivate = document.getElementById(firstInvalidTabId);
                if (contentToActivate) {
                    contentToActivate.classList.add('active');
                    contentToActivate.hidden = false;
                }
            }
            if (firstInvalid && typeof firstInvalid.focus === 'function') {
                firstInvalid.focus();
            }
        }
    });
});
