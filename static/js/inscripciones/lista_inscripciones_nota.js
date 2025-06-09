document.addEventListener('DOMContentLoaded', function () {
  // Maneja el click en el botón "Agregar Notas" para mostrar el modal
  document.querySelectorAll('.agregar-notas-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var inscripcionId = btn.getAttribute('data-inscripcion');
      document.getElementById('modal_inscripcion_id').value = inscripcionId;
      var modal = new bootstrap.Modal(document.getElementById('modalNotasCertificacion'));
      modal.show();
    });
  });

  // Opcional: manejar el submit del formulario del modal
  document.getElementById('formNotasCertificacion').addEventListener('submit', function(e) {
    // Aquí puedes manejar el envío por AJAX si lo deseas.
    // Por defecto, el formulario se enviará normalmente.
    // e.preventDefault();
  });
});