document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('convocatoria-form');
    const submitBtn = form.querySelector('button[type="submit"]');

    // Crear o reutilizar el contenedor de mensajes de error
    let errorDiv = document.createElement('div');
    errorDiv.style.color = 'red';
    errorDiv.style.marginBottom = '1rem';
    errorDiv.style.display = 'none';
    errorDiv.setAttribute('id', 'form-error-msg');
    submitBtn.parentNode.insertBefore(errorDiv, submitBtn);

    form.addEventListener('submit', function(e) {
        console.log('Submit presionado');
        submitBtn.disabled = true;
        errorDiv.style.display = 'none';
        errorDiv.textContent = '';

        // Selecciona todos los inputs, selects y textareas visibles dentro del formulario
        const fields = Array.from(form.querySelectorAll('input, select, textarea')).filter(el => {
            // Solo los visibles y habilitados
            return el.offsetParent !== null && !el.disabled && el.type !== 'hidden';
        });

        console.log('Campos visibles a validar:', fields.map(f => ({name: f.name, id: f.id, value: f.value, type: f.type})));

        let valid = true;
        let firstInvalid = null;
        for (const field of fields) {
            if (field.type === 'checkbox') {
                if (field.required && !field.checked) {
                    valid = false;
                    firstInvalid = field;
                    console.log('Campo checkbox inválido:', field);
                    break;
                }
            } else if (!field.value) {
                valid = false;
                firstInvalid = field;
                console.log('Campo vacío:', field);
                break;
            }
        }

        if (!valid) {
            e.preventDefault();
            submitBtn.disabled = false;
            let label = '';
            if (firstInvalid) {
                const labelEl = form.querySelector(`label[for="${firstInvalid.id}"]`);
                label = labelEl ? labelEl.textContent : firstInvalid.name || 'Este campo';
            }
            errorDiv.textContent = `Por favor complete el campo obligatorio: ${label}.`;
            errorDiv.style.display = 'block';
            if (firstInvalid && typeof firstInvalid.focus === 'function') {
                firstInvalid.focus();
            }
            console.log('Formulario NO enviado. Motivo:', errorDiv.textContent);
        } else {
            console.log('Formulario válido. Enviando...');
        }
        // Si es válido, el submit sigue y el botón queda bloqueado
    });
});
