document.addEventListener('DOMContentLoaded', function () {
    const selectAll = document.getElementById('selectAll');
    const checkboxes = document.querySelectorAll('.usuario-checkbox');

    selectAll.addEventListener('change', function () {
      checkboxes.forEach(cb => cb.checked = selectAll.checked);
    });
  });

  function confirmarEliminacion() {
    const seleccionados = document.querySelectorAll('.usuario-checkbox:checked');
    if (seleccionados.length === 0) {
      alert("Debes seleccionar al menos un usuario.");
      return false;
    }
    return confirm("¿Estás seguro de que deseas eliminar los usuarios seleccionados?");
  }