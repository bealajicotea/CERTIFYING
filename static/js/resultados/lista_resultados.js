console.log('Cargando script de filtros...');
console.log('Script de filtros cargado'); // Debe aparecer siempre

document.addEventListener('DOMContentLoaded', function () {
  // --- Nuevo manejo de filtros con checkboxes ---
  const filtroMap = {
    'facultad': 0,
    'grupo': 1,
    'anio_escolar': 2,
    'tipo_convocatoria': 3,
    'nivel': 4
  };

  function actualizarFiltros() {
    const seleccionados = Array.from(document.querySelectorAll('.filtro-checkbox:checked')).map(cb => cb.value);
    Object.entries(filtroMap).forEach(([filtro, idx]) => {
      const div = document.querySelectorAll('.filtros .col-md-2')[idx];
      const select = div ? div.querySelector('select') : null;
      if (div) {
        if (seleccionados.includes(filtro)) {
          div.classList.remove('d-none');
        } else {
          // Solo limpiar y enviar si el filtro estaba visible y ahora se oculta
          if (!div.classList.contains('d-none') && select && select.value !== "") {
            select.value = "";
            // Dispara el evento change para que se envíe el formulario
            select.dispatchEvent(new Event('change', { bubbles: true }));
          }
          div.classList.add('d-none');
        }
      }
    });
  }

  document.querySelectorAll('.filtro-checkbox').forEach(cb => {
    cb.addEventListener('change', function () {
      actualizarFiltros();
      // Actualiza el input oculto de filtros activos
      var seleccionados = Array.from(document.querySelectorAll('.filtro-checkbox:checked')).map(cb => cb.value);
      document.getElementById('filtros_activos').value = seleccionados.join(',');
    });
  });

  // Inicializa los filtros al cargar
  actualizarFiltros();

  // Evitar que el dropdown se cierre al hacer clic en los checkboxes de filtros
  document.querySelectorAll('.filtro-checkbox').forEach(cb => {
    cb.addEventListener('click', function (event) {
      event.stopPropagation();
    });
  });

  document.querySelectorAll('.form-check-label').forEach(label => {
    label.addEventListener('click', function (event) {
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
});

document.addEventListener('DOMContentLoaded', function () {
  const ids = [
    'filtroFacultad',
    'filtroGrupo',
    'filtroAnio',
    'filtroTipo',
    'filtroNivel'
  ];

  ids.forEach(function (id) {
    const cb = document.getElementById(id);
    if (cb) {
      cb.addEventListener('mousedown', function (event) {
        event.stopPropagation();
      });
      cb.addEventListener('click', function (event) {
        event.stopPropagation();
      });
    }
  });
});

document.addEventListener('DOMContentLoaded', function () {
  // Leer filtros activos desde el input oculto
  var filtrosActivos = document.getElementById('filtros_activos');
  if (filtrosActivos) {
    var activos = filtrosActivos.value.split(',').map(f => f.trim()).filter(f => f);
    activos.forEach(function (filtro) {
      var cb = document.querySelector('.filtro-checkbox[value="' + filtro + '"]');
      if (cb) cb.checked = true;
      var filtroMap = {
        'facultad': 0,
        'grupo': 1,
        'anio_escolar': 2,
        'tipo_convocatoria': 3,
        'nivel': 4
      };
      var idx = filtroMap[filtro];
      if (typeof idx !== 'undefined') {
        var div = document.querySelectorAll('.filtros .col-md-2')[idx];
        if (div) div.classList.remove('d-none');
      }
    });
  }

  document.querySelectorAll('.filtro-checkbox').forEach(cb => {
    cb.addEventListener('change', function () {
      var seleccionados = Array.from(document.querySelectorAll('.filtro-checkbox:checked')).map(cb => cb.value);
      document.getElementById('filtros_activos').value = seleccionados.join(',');
    });
  });
});
