// ==============================
// Sistema de Modales Personalizados
// ==============================

function showModal(type, title, message, buttons = []) {
  const modal = document.getElementById("customModal");
  const modalIcon = document.getElementById("modalIcon");
  const modalTitle = document.getElementById("modalTitle");
  const modalMessage = document.getElementById("modalMessage");
  const modalButtons = document.getElementById("modalButtons");

  // Configurar ícono según el tipo
  const icons = {
    success: "✅",
    error: "❌",
    warning: "⚠️",
    info: "ℹ️",
    question: "❓",
  };

  modalIcon.textContent = icons[type] || icons.info;
  modalTitle.textContent = title;
  modalMessage.textContent = message;

  // Configurar botones
  modalButtons.innerHTML = "";
  if (buttons.length === 0) {
    buttons = [
      {
        text: "Aceptar",
        class: "modal-btn-primary",
        callback: () => closeModal(),
      },
    ];
  }

  buttons.forEach((btn) => {
    const button = document.createElement("button");
    button.textContent = btn.text;
    button.className = `modal-btn ${btn.class}`;
    button.onclick = () => {
      if (btn.callback) btn.callback();
      closeModal();
    };
    modalButtons.appendChild(button);
  });

  modal.style.display = "block";
}

function closeModal() {
  document.getElementById("customModal").style.display = "none";
}

// Cerrar modal al hacer clic fuera de él
window.onclick = function (event) {
  const modal = document.getElementById("customModal");
  if (event.target === modal) {
    closeModal();
  }
};

// ==============================
// Variables globales
// ==============================
let manoObra = [];
let cifs = [];

// ==============================
// Funciones para Mano de Obra
// ==============================

function renderizarTablaManoObra() {
  const tbody = document.getElementById("tablaManoObra");

  if (manoObra.length === 0) {
    tbody.innerHTML = `
    <tr>
      <td colspan="6" class="text-center text-muted" style="padding: 2rem;">
        No hay registros aún
      </td>
    </tr>
  `;
    actualizarTotales();
    return;
  }

  tbody.innerHTML = manoObra
    .map(
      (trabajador, index) => `
    <tr>
      <td>${trabajador.nombre}</td>
      <td>${trabajador.cargo}</td>
      <td>$${parseFloat(trabajador.costo).toFixed(2)}</td>
      <td>${trabajador.fecha}</td>
      <td>${trabajador.observaciones || "N/A"}</td>
      <td>
        <button
          type="button"
          class="btn btn-sm btn-warning"
          onclick="editarTrabajador(${index})"
          title="Editar"
        >
          ✏️
        </button>
        <button
          type="button"
          class="btn btn-sm btn-danger"
          onclick="eliminarTrabajador(${index})"
          title="Eliminar"
        >
          🗑️
        </button>
      </td>
    </tr>
  `
    )
    .join("");

  actualizarTotales();
}

function editarTrabajador(index) {
  const trabajador = manoObra[index];

  // Llenar el formulario con los datos existentes
  document.getElementById("nombre_trabajador").value = trabajador.nombre;
  document.getElementById("cargo").value = trabajador.cargo;
  document.getElementById("costo_mensual").value = trabajador.costo;
  document.getElementById("fecha_mo").value = trabajador.fecha;
  document.getElementById("observaciones_mo").value =
    trabajador.observaciones || "";

  // Eliminar el registro actual
  manoObra.splice(index, 1);
  renderizarTablaManoObra();

  // Scroll hacia el formulario
  document
    .getElementById("formManoObra")
    .scrollIntoView({ behavior: "smooth" });
}

function eliminarTrabajador(index) {
  showModal(
    "question",
    "¿Eliminar Trabajador?",
    "¿Está seguro que desea eliminar este registro? Esta acción no se puede deshacer.",
    [
      {
        text: "Cancelar",
        class: "modal-btn-secondary",
        callback: () => {},
      },
      {
        text: "Eliminar",
        class: "modal-btn-danger",
        callback: () => {
          manoObra.splice(index, 1);
          renderizarTablaManoObra();
          showModal(
            "success",
            "¡Eliminado!",
            "El trabajador ha sido eliminado exitosamente."
          );
        },
      },
    ]
  );
}

// ==============================
// Funciones para CIF
// ==============================

function renderizarTablaCIF() {
  const tbody = document.getElementById("tablaCIF");

  if (cifs.length === 0) {
    tbody.innerHTML = `
    <tr>
      <td colspan="6" class="text-center text-muted" style="padding: 2rem;">
        No hay registros aún
      </td>
    </tr>
  `;
    actualizarTotales();
    return;
  }

  tbody.innerHTML = cifs
    .map(
      (cif, index) => `
    <tr>
      <td>${cif.concepto}</td>
      <td><span class="badge bg-info">${cif.categoria}</span></td>
      <td>$${parseFloat(cif.monto).toFixed(2)}</td>
      <td>${cif.fecha}</td>
      <td>${cif.descripcion || "N/A"}</td>
      <td>
        <button
          type="button"
          class="btn btn-sm btn-warning"
          onclick="editarCIF(${index})"
          title="Editar"
        >
          ✏️
        </button>
        <button
          type="button"
          class="btn btn-sm btn-danger"
          onclick="eliminarCIF(${index})"
          title="Eliminar"
        >
          🗑️
        </button>
      </td>
    </tr>
  `
    )
    .join("");

  actualizarTotales();
}

function editarCIF(index) {
  const cif = cifs[index];

  // Llenar el formulario con los datos existentes
  document.getElementById("concepto").value = cif.concepto;
  document.getElementById("categoria").value = cif.categoria;
  document.getElementById("monto").value = cif.monto;
  document.getElementById("fecha_cif").value = cif.fecha;
  document.getElementById("descripcion").value = cif.descripcion || "";

  // Eliminar el registro actual
  cifs.splice(index, 1);
  renderizarTablaCIF();

  // Scroll hacia el formulario
  document.getElementById("formCIF").scrollIntoView({ behavior: "smooth" });
}

function eliminarCIF(index) {
  showModal(
    "question",
    "¿Eliminar Costo Indirecto?",
    "¿Está seguro que desea eliminar este registro? Esta acción no se puede deshacer.",
    [
      {
        text: "Cancelar",
        class: "modal-btn-secondary",
        callback: () => {},
      },
      {
        text: "Eliminar",
        class: "modal-btn-danger",
        callback: () => {
          cifs.splice(index, 1);
          renderizarTablaCIF();
          showModal(
            "success",
            "¡Eliminado!",
            "El costo indirecto ha sido eliminado exitosamente."
          );
        },
      },
    ]
  );
}

// ==============================
// Funciones para cálculos
// ==============================

function calcularTotalMOD() {
  return manoObra.reduce(
    (total, trabajador) => total + parseFloat(trabajador.costo),
    0
  );
}

function calcularTotalCIF() {
  return cifs.reduce((total, cif) => total + parseFloat(cif.monto), 0);
}

function calcularTasaCIF() {
  const totalCIF = calcularTotalCIF();
  const totalMOD = calcularTotalMOD();

  if (totalMOD === 0) return 0;
  return (totalCIF / totalMOD) * 100;
}

function actualizarTotales() {
  const totalMOD = calcularTotalMOD();
  const totalCIF = calcularTotalCIF();
  const tasaCIF = calcularTasaCIF();

  // Actualizar en las tablas
  document.getElementById("totalMOD").textContent = `$${totalMOD.toFixed(2)}`;
  document.getElementById("totalCIF").textContent = `$${totalCIF.toFixed(2)}`;

  // Actualizar en el resumen
  document.getElementById("resumenMOD").textContent = `$${totalMOD.toFixed(
    2
  )}`;
  document.getElementById("resumenCIF").textContent = `$${totalCIF.toFixed(
    2
  )}`;
  document.getElementById("tasaCIF").textContent = `${tasaCIF.toFixed(2)}%`;
}

// ==============================
// Función para exportar PDF
// ==============================
function exportarPDF() {
  showModal(
    "info",
    "Exportar PDF",
    `Resumen de Costos:\n\nTotal MOD: $${calcularTotalMOD().toFixed(
      2
    )}\nTotal CIF: $${calcularTotalCIF().toFixed(
      2
    )}\nTasa CIF: ${calcularTasaCIF().toFixed(
      2
    )}%\n\nFuncionalidad en desarrollo...`
  );
}

// ==============================
// Inicialización
// ==============================
document.addEventListener("DOMContentLoaded", function () {
  // Establecer fecha actual por defecto
  const hoy = new Date().toISOString().split("T")[0];
  document.getElementById("fecha_mo").value = hoy;
  document.getElementById("fecha_cif").value = hoy;

  // Formulario Mano de Obra
  document
    .getElementById("formManoObra")
    .addEventListener("submit", function (e) {
      e.preventDefault();

      const nombre = document
        .getElementById("nombre_trabajador")
        .value.trim();
      const cargo = document.getElementById("cargo").value.trim();
      const costo = document.getElementById("costo_mensual").value;
      const fecha = document.getElementById("fecha_mo").value;
      const observaciones = document
        .getElementById("observaciones_mo")
        .value.trim();

      if (!nombre || !cargo || !costo || !fecha) {
        showModal(
          "error",
          "Campos Incompletos",
          "Por favor, complete todos los campos obligatorios."
        );
        return;
      }

      if (parseFloat(costo) <= 0) {
        showModal(
          "error",
          "Valor Inválido",
          "El costo debe ser mayor a cero."
        );
        return;
      }

      const trabajador = {
        nombre,
        cargo,
        costo: parseFloat(costo),
        fecha,
        observaciones,
      };

      manoObra.push(trabajador);
      renderizarTablaManoObra();
      this.reset();
      document.getElementById("fecha_mo").value = hoy;
      showModal(
        "success",
        "¡Registro Exitoso!",
        "El trabajador ha sido agregado correctamente."
      );
    });

  // Formulario CIF
  document.getElementById("formCIF").addEventListener("submit", function (e) {
    e.preventDefault();

    const concepto = document.getElementById("concepto").value.trim();
    const categoria = document.getElementById("categoria").value;
    const monto = document.getElementById("monto").value;
    const fecha = document.getElementById("fecha_cif").value;
    const descripcion = document.getElementById("descripcion").value.trim();

    if (!concepto || !categoria || !monto || !fecha) {
      showModal(
        "error",
        "Campos Incompletos",
        "Por favor, complete todos los campos obligatorios."
      );
      return;
    }

    if (parseFloat(monto) <= 0) {
      showModal("error", "Valor Inválido", "El monto debe ser mayor a cero.");
      return;
    }

    const cif = {
      concepto,
      categoria,
      monto: parseFloat(monto),
      fecha,
      descripcion,
    };

    cifs.push(cif);
    renderizarTablaCIF();
    this.reset();
    document.getElementById("fecha_cif").value = hoy;
    showModal(
      "success",
      "¡Registro Exitoso!",
      "El costo indirecto ha sido agregado correctamente."
    );
  });

  // Renderizar tablas iniciales
  renderizarTablaManoObra();
  renderizarTablaCIF();
});