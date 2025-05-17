document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.getElementById('toggleCertInfoBtn');
    const collapseEl = document.getElementById('moreCertInfo');

    collapseEl.addEventListener('show.bs.collapse', function () {
      toggleBtn.textContent = 'Leer menos';
    });

    collapseEl.addEventListener('hide.bs.collapse', function () {
      toggleBtn.textContent = 'Leer más';
    });
  });

console.log("Pagina principal cargada");