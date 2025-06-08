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

  // Seleccionar/deseleccionar todos los checkboxes de inscripciones
  const selectAll = document.getElementById('selectAllInscripciones');
  if (selectAll) {
    selectAll.addEventListener('change', function () {
      document.querySelectorAll('.inscripcion-checkbox').forEach(cb => cb.checked = selectAll.checked);
    });
  }

  document.querySelectorAll('.agregar-nota-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const wrapper = btn.closest('.agregar-nota-wrapper');
      btn.style.display = 'none';
      wrapper.querySelector('.inputs-agregar-nota').style.display = 'inline-block';
      wrapper.querySelector('select[name="nota"]').focus();
    });
  });

  document.querySelectorAll('.aceptar-nota-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const wrapper = btn.closest('.agregar-nota-wrapper');
      const inscripcionId = wrapper.querySelector('input[name="inscripcion_id"]').value;
      const nota = wrapper.querySelector('select[name="nota"]').value;

      document.getElementById('elemento_id').value = inscripcionId;
      document.getElementById('codigo').value = nota;

      const formOculto = document.getElementById('formOculto');
      formOculto.action = formOculto.getAttribute('data-action-url'); // Personalízalo si lo haces dinámico
      formOculto.method = "post";

      let csrfInput = formOculto.querySelector('input[name="csrfmiddlewaretoken"]');
      if (!csrfInput) {
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]');
        if (csrfToken) {
          csrfInput = csrfToken.cloneNode();
          formOculto.prepend(csrfInput);
        }
      }

      formOculto.submit();
    });
  });

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
  console.log('Cantidad de filtros encontrados:', filtros.length);
  filtros.forEach(cb => {
    cb.addEventListener('click', function (event) {
      console.log('Checkbox filtro clickeado:', cb.value);
      event.stopPropagation();
    });
  });
});

// Script de refuerzo por ID
document.addEventListener('DOMContentLoaded', function () {
  console.log('Script de filtros cargado (por ID)');

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
