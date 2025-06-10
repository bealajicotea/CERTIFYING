document.addEventListener('DOMContentLoaded', function() {
    const tipoUsuario = document.getElementById('id-tipo_usuario');
    const grupoDiv = document.getElementById('id-grupo')?.parentNode;
    const anioEscolarDiv = document.getElementById('id-anio_escolar')?.parentNode;

    function updateCamposAcademicos() {
        if (tipoUsuario && tipoUsuario.value === 'profesor') {
            if (grupoDiv) grupoDiv.style.display = 'none';
            if (anioEscolarDiv) anioEscolarDiv.style.display = 'none';
        } else {
            if (grupoDiv) grupoDiv.style.display = '';
            if (anioEscolarDiv) anioEscolarDiv.style.display = '';
        }
    }

    if (tipoUsuario) {
        tipoUsuario.addEventListener('change', updateCamposAcademicos);
        updateCamposAcademicos();
    }
});