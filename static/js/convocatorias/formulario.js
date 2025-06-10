document.addEventListener('DOMContentLoaded', function() {
    const tipoSelect = document.getElementById('id-tipo');
    const fechaCol = document.getElementById('fecha-col');
    const nivelDiv = document.getElementById('nivel-div');
    const fechaInput = document.getElementById('id-fecha');

    function updateFields() {
        if (tipoSelect.value === 'curso') {
            fechaCol.style.display = 'none';
            fechaInput.required = false;
            nivelDiv.style.display = '';
        } else {
            fechaCol.style.display = '';
            fechaInput.required = true;
            nivelDiv.style.display = 'none';
        }
    }

    tipoSelect.addEventListener('change', updateFields);
    updateFields();
});
