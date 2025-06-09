// static/js/resultados/lista_resultados.js
console.log('Cargando script de filtros para resultados...');

document.addEventListener('DOMContentLoaded', function () {
  // --- Nuevo manejo de filtros con checkboxes ---
  const filtroMap = {
    'tipo_examen': 0, // Corresponds to the first d-none col-md-2 div
    'nivel_nota': 1   // Corresponds to the second d-none col-md-2 div
    // Add more mappings for new filters
  };

  function actualizarFiltros() {
    const seleccionados = Array.from(document.querySelectorAll('.filtro-checkbox:checked')).map(cb => cb.value);
    Object.entries(filtroMap).forEach(([filtro, idx]) => {
      // Assuming the filter forms are direct children of .filtros and then have col-md-2
      const div = document.querySelector('.filtros form.row.g-2 .col-md-2:nth-child(' + (idx + 1) + ')');
      if (div) {
        if (seleccionados.includes(filtro)) {
          div.classList.remove('d-none');
        } else {
          div.classList.add('d-none');
        }
      }
    });
  }

  document.querySelectorAll('.filtro-checkbox').forEach(cb => {
    cb.addEventListener('change', actualizarFiltros);
  });
  // Call on load to set initial state based on checked checkboxes
  actualizarFiltros();

  // Evitar que el dropdown se cierre al hacer clic en los checkboxes de filtros
  document.querySelectorAll('.filtro-checkbox').forEach(cb => {
    cb.addEventListener('click', function (event) {
      console.log('Checkbox filtro clickeado:', cb.value); // Depuración
      event.stopPropagation();
    });
  });

  document.querySelectorAll('.form-check-label').forEach(label => {
    label.addEventListener('click', function (event) {
      console.log('Label filtro clickeado:', label.htmlFor); // Depuración
      event.stopPropagation();
    });
  });

  // Seleccionar/deseleccionar todos los checkboxes de resultados
  const selectAll = document.getElementById('selectAllResultados');
  if (selectAll) {
    selectAll.addEventListener('change', function () {
      document.querySelectorAll('.resultado-checkbox').forEach(cb => cb.checked = selectAll.checked);
    });
  }

  // Refuerzo para evitar cierre del dropdown en clicks y mousedowns
  document.querySelectorAll('.filtro-checkbox').forEach(cb => {
    cb.addEventListener('mousedown', function (event) {
      console.log('Checkbox filtro mousedown:', cb.value); // Depuración
      event.stopPropagation();
    });
    cb.addEventListener('click', function (event) {
      console.log('Checkbox filtro click:', cb.value); // Depuración
      event.stopPropagation();
    });
  });

  document.querySelectorAll('.form-check-label').forEach(label => {
    label.addEventListener('mousedown', function (event) {
      console.log('Label filtro mousedown:', label.htmlFor); // Depuración
      event.stopPropagation();
    });
    label.addEventListener('click', function (event) {
      console.log('Label filtro click:', label.htmlFor); // Depuración
      event.stopPropagation();
    });
  });

  const filtros = document.querySelectorAll('.filtro-checkbox');
  console.log('Cantidad de filtros de resultados encontrados:', filtros.length);
  filtros.forEach(cb => {
    cb.addEventListener('click', function (event) {
      console.log('Checkbox filtro clickeado:', cb.value);
      event.stopPropagation();
    });
  });
});

// Script de refuerzo por ID para filtros (similar al de inscripciones)
document.addEventListener('DOMContentLoaded', function () {
  console.log('Script de filtros de resultados cargado (por ID)');

  const ids = [
    'filtroTipoExamen',
    'filtroNivelNota'
    // Add more IDs for new filters
  ];

  ids.forEach(function (id) {
    const cb = document.getElementById(id);
    if (cb) {
      cb.addEventListener('mousedown', function (event) {
        console.log('mousedown en:', id);
        event.stopPropagation();
      });
      cb.addEventListener('click', function (event) {
        console.log('click en:', id);
        event.stopPropagation();
      });
    } else {
      console.log('No se encontró el checkbox con id:', id);
    }
  });
});