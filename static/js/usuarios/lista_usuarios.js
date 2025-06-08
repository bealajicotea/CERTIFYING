document.addEventListener('DOMContentLoaded', function () {
  console.log('Script de lista_usuarios cargado.');

  /**
   * ------------------------------------------------------------------------
   * MANEJO DE LA VISIBILIDAD DE LOS FILTROS
   * Muestra u oculta los <select> de filtros basados en los checkboxes
   * marcados en el dropdown.
   * ------------------------------------------------------------------------
   */
  const filtroCheckboxes = document.querySelectorAll('.filtro-checkbox');

  function actualizarVisibilidadFiltros() {
    const filtrosSeleccionados = Array.from(document.querySelectorAll('.filtro-checkbox:checked')).map(cb => cb.value);
    document.querySelectorAll('.filtros [data-filtro]').forEach(divFiltro => {
      const nombreFiltro = divFiltro.getAttribute('data-filtro');
      if (filtrosSeleccionados.includes(nombreFiltro)) {
        divFiltro.classList.remove('d-none');
      } else {
        divFiltro.classList.add('d-none');
      }
    });
  }

  filtroCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', actualizarVisibilidadFiltros);
  });

  actualizarVisibilidadFiltros();


  /**
   * ------------------------------------------------------------------------
   * [CORREGIDO] EVITAR CIERRE DEL DROPDOWN DE FILTROS
   * Previene que el menú desplegable se cierre al hacer clic en un
   * checkbox o su etiqueta, deteniendo la propagación del evento 'click'.
   * ------------------------------------------------------------------------
   */
  const elementosDelDropdown = document.querySelectorAll('.dropdown-menu .filtro-checkbox, .dropdown-menu .form-check-label');

  elementosDelDropdown.forEach(elemento => {
    elemento.addEventListener('click', function (event) {
        console.log('Click dentro del dropdown, deteniendo propagación.'); // Para depuración
        event.stopPropagation();
    });
  });


  /**
   * ------------------------------------------------------------------------
   * SELECCIONAR / DESELECCIONAR TODOS LOS USUARIOS
   * Controla el checkbox principal para marcar o desmarcar todos los
   * checkboxes de la lista de usuarios.
   * ------------------------------------------------------------------------
   */
  const selectAll = document.getElementById('selectAll');
  if (selectAll) {
    selectAll.addEventListener('change', function () {
      document.querySelectorAll('.usuario-checkbox').forEach(checkbox => {
        checkbox.checked = this.checked;
      });
    });
  }
});