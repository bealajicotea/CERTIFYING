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
    // Obtiene una lista con los valores de los filtros seleccionados (ej: ['facultad', 'grupo'])
    const filtrosSeleccionados = Array.from(document.querySelectorAll('.filtro-checkbox:checked')).map(cb => cb.value);

    // Itera sobre cada div de filtro que tenga el atributo 'data-filtro'
    document.querySelectorAll('.filtros [data-filtro]').forEach(divFiltro => {
      const nombreFiltro = divFiltro.getAttribute('data-filtro');
      
      // Si el filtro está en la lista de seleccionados, lo muestra. Si no, lo oculta.
      if (filtrosSeleccionados.includes(nombreFiltro)) {
        divFiltro.classList.remove('d-none');
      } else {
        divFiltro.classList.add('d-none');
      }
    });
  }

  // Añade el evento 'change' a cada checkbox de filtro
  filtroCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', actualizarVisibilidadFiltros);
  });

  // Llama a la función una vez al cargar la página para establecer el estado inicial correcto
  actualizarVisibilidadFiltros();


  /**
   * ------------------------------------------------------------------------
   * EVITAR CIERRE DEL DROPDOWN DE FILTROS
   * Previene que el menú desplegable de filtros se cierre al hacer clic
   * en un checkbox o su etiqueta.
   * ------------------------------------------------------------------------
   */
  const dropdownContent = document.querySelector('.dropdown-menu');
  if (dropdownContent) {
    dropdownContent.addEventListener('click', function (event) {
        // Detiene la propagación del evento 'click' para que no llegue al dropdown y lo cierre
        event.stopPropagation();
    });
  }


  /**
   * ------------------------------------------------------------------------
   * SELECCIONAR / DESELECCIONAR TODOS LOS USUARIOS
   * Controla el checkbox principal para marcar o desmarcar todos los
   * checkboxes de la lista de usuarios.
   * ------------------------------------------------------------------------
   */
  const selectAll = document.getElementById('selectAll'); // ID del checkbox principal
  if (selectAll) {
    selectAll.addEventListener('change', function () {
      // Busca todos los checkboxes de usuario y sincroniza su estado con el del checkbox principal
      document.querySelectorAll('.usuario-checkbox').forEach(checkbox => {
        checkbox.checked = this.checked;
      });
    });
  }
});