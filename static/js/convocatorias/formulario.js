document.addEventListener('DOMContentLoaded', function() {
    const tipoSelect = document.getElementById('id-tipo');
    const fechaRow = document.getElementById('fecha-row');
    const nivelDiv = document.getElementById('nivel-div');

    function updateFields() {
        if (tipoSelect.value === 'curso') {
            fechaRow.style.display = 'none';
            nivelDiv.style.display = '';
        } else {
            fechaRow.style.display = '';
            nivelDiv.style.display = 'none';
        }
    }

    tipoSelect.addEventListener('change', updateFields);
    updateFields();
});
