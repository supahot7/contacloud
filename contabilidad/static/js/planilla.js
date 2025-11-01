// ==============================
// Variables globales
// ==============================
let planillaEmpleados = [];

// Constantes para cálculos
const TASA_ISSS = 0.075; // 7.5%
const TASA_AFP = 0.0725; // 7.25%
const TASA_INCAF = 0.01; // 1%

// Porcentajes de vacaciones según años trabajados
const VACACIONES = {
  '1-3': 0.30,
  '3-10': 0.50,
  '10+': 0.50
};

// Porcentajes de aguinaldo según años trabajados
const AGUINALDO = {
  '1-3': 0.50,
  '3-10': 0.57,
  '10+': 0.60
};

// ==============================
// Función para calcular planilla
// ==============================
function calcularPlanilla() {
  const salarioNominal = parseFloat(document.getElementById('salario_nominal').value);
  const diasTrabajados = parseInt(document.getElementById('dias_trabajados').value);
  const anosTrabajos = document.querySelector('input[name="anos_trabajados"]:checked').value;

  if (!salarioNominal || !diasTrabajados) {
    alert('Por favor, complete todos los campos requeridos.');
    return;
  }

  // Validaciones
  if (salarioNominal <= 0) {
    alert('El salario debe ser mayor a 0.');
    return;
  }

  if (diasTrabajados < 1 || diasTrabajados > 31) {
    alert('Los días trabajados deben estar entre 1 y 31.');
    return;
  }

  // Cálculos
  const costoSemanaSalarial = salarioNominal;
  const septimo = salarioNominal / 6;
  const vacaciones = salarioNominal * VACACIONES[anosTrabajos];
  const aguinaldo = salarioNominal * AGUINALDO[anosTrabajos];
  const salarioCancelado = costoSemanaSalarial + septimo + vacaciones + aguinaldo;
  
  const isss = salarioCancelado * TASA_ISSS;
  const afp = salarioCancelado * TASA_AFP;
  const incaf = salarioCancelado * TASA_INCAF;
  
  const salarioTotalSemanal = salarioCancelado - (isss + afp + incaf);
  const salarioTotalMensual = (salarioTotalSemanal * diasTrabajados) / 7;

  // Mostrar resultados
  document.getElementById('res_sueldo_nominal').textContent = `$${salarioNominal.toFixed(2)}`;
  document.getElementById('res_costo_semana').textContent = `$${costoSemanaSalarial.toFixed(2)}`;
  document.getElementById('res_septimo').textContent = `$${septimo.toFixed(2)}`;
  document.getElementById('res_vacaciones').textContent = `$${vacaciones.toFixed(2)}`;
  document.getElementById('res_aguinaldo').textContent = `$${aguinaldo.toFixed(2)}`;
  document.getElementById('res_salario_cancelado').textContent = `$${salarioCancelado.toFixed(2)}`;
  document.getElementById('res_isss').textContent = `$${isss.toFixed(2)}`;
  document.getElementById('res_afp').textContent = `$${afp.toFixed(2)}`;
  document.getElementById('res_incaf').textContent = `$${incaf.toFixed(2)}`;
  document.getElementById('res_total_semanal').textContent = `$${salarioTotalSemanal.toFixed(2)}`;
  document.getElementById('res_total_mensual').textContent = `$${salarioTotalMensual.toFixed(2)}`;

  // Guardar cálculo actual
  window.calculoActual = {
    nombre: document.getElementById('nombre_empleado').value,
    puesto: document.getElementById('puesto').value,
    salarioNominal,
    salarioTotalSemanal,
    salarioTotalMensual,
    diasTrabajados,
    anosTrabajos,
    costoSemanaSalarial,
    septimo,
    vacaciones,
    aguinaldo,
    salarioCancelado,
    isss,
    afp,
    incaf
  };
}

// ==============================
// Función para agregar a planilla
// ==============================
function agregarAPlanilla() {
  if (!window.calculoActual) {
    alert('Primero debe calcular la planilla de un empleado.');
    return;
  }

  const empleado = window.calculoActual;

  // Validar que se haya seleccionado un empleado
  if (!empleado.nombre || empleado.nombre === '') {
    alert('Debe seleccionar un empleado.');
    return;
  }

  if (!empleado.puesto || empleado.puesto === '') {
    alert('Debe seleccionar un puesto.');
    return;
  }

  // Verificar si el empleado ya existe
  const existe = planillaEmpleados.find(e => e.nombre === empleado.nombre);
  if (existe) {
    if (!confirm(`${empleado.nombre} ya está en la planilla. ¿Desea actualizarlo?`)) {
      return;
    }
    // Eliminar el anterior
    planillaEmpleados = planillaEmpleados.filter(e => e.nombre !== empleado.nombre);
  }

  planillaEmpleados.push(empleado);
  renderizarPlanillaCompleta();
  alert(`${empleado.nombre} agregado a la planilla exitosamente.`);
  
  // Limpiar formulario
  document.getElementById('formPlanilla').reset();
  limpiarResultados();
}

// ==============================
// Función para renderizar planilla completa
// ==============================
function renderizarPlanillaCompleta() {
  const tbody = document.getElementById('tbodyPlanilla');
  
  if (planillaEmpleados.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="6" class="text-center text-muted" style="padding: 2rem;">
          No hay empleados en la planilla. Calcula y agrega empleados para comenzar.
        </td>
      </tr>
    `;
    document.getElementById('total_semanal_planilla').textContent = '$0.00';
    document.getElementById('total_mensual_planilla').textContent = '$0.00';
    return;
  }

  let totalSemanal = 0;
  let totalMensual = 0;

  tbody.innerHTML = planillaEmpleados.map((emp, index) => {
    totalSemanal += emp.salarioTotalSemanal;
    totalMensual += emp.salarioTotalMensual;
    
    return `
      <tr>
        <td>${emp.nombre}</td>
        <td>${emp.puesto}</td>
        <td class="text-end">$${emp.salarioNominal.toFixed(2)}</td>
        <td class="text-end">$${emp.salarioTotalSemanal.toFixed(2)}</td>
        <td class="text-end">$${emp.salarioTotalMensual.toFixed(2)}</td>
        <td class="text-center">
          <button class="btn btn-sm btn-danger" onclick="eliminarEmpleado(${index})" title="Eliminar">
            🗑️ Eliminar
          </button>
        </td>
      </tr>
    `;
  }).join('');

  document.getElementById('total_semanal_planilla').textContent = `$${totalSemanal.toFixed(2)}`;
  document.getElementById('total_mensual_planilla').textContent = `$${totalMensual.toFixed(2)}`;
}

// ==============================
// Función para eliminar empleado
// ==============================
function eliminarEmpleado(index) {
  const empleado = planillaEmpleados[index];
  if (confirm(`¿Está seguro que desea eliminar a ${empleado.nombre} de la planilla?`)) {
    planillaEmpleados.splice(index, 1);
    renderizarPlanillaCompleta();
    alert('Empleado eliminado exitosamente.');
  }
}

// ==============================
// Función para limpiar resultados
// ==============================
function limpiarResultados() {
  document.getElementById('res_sueldo_nominal').textContent = '$0.00';
  document.getElementById('res_costo_semana').textContent = '$0.00';
  document.getElementById('res_septimo').textContent = '$0.00';
  document.getElementById('res_vacaciones').textContent = '$0.00';
  document.getElementById('res_aguinaldo').textContent = '$0.00';
  document.getElementById('res_salario_cancelado').textContent = '$0.00';
  document.getElementById('res_isss').textContent = '$0.00';
  document.getElementById('res_afp').textContent = '$0.00';
  document.getElementById('res_incaf').textContent = '$0.00';
  document.getElementById('res_total_semanal').textContent = '$0.00';
  document.getElementById('res_total_mensual').textContent = '$0.00';
  window.calculoActual = null;
}

// ==============================
// Función para exportar a Excel
// ==============================
function exportarExcel() {
  if (planillaEmpleados.length === 0) {
    alert('No hay empleados en la planilla para exportar.');
    return;
  }

  // Crear encabezados
  let csv = 'Nombre,Puesto,Salario Nominal,Total Semanal,Total Mensual\n';

  // Agregar datos
  planillaEmpleados.forEach(emp => {
    csv += `${emp.nombre},${emp.puesto},${emp.salarioNominal.toFixed(2)},${emp.salarioTotalSemanal.toFixed(2)},${emp.salarioTotalMensual.toFixed(2)}\n`;
  });

  // Calcular totales
  const totalSemanal = planillaEmpleados.reduce((sum, emp) => sum + emp.salarioTotalSemanal, 0);
  const totalMensual = planillaEmpleados.reduce((sum, emp) => sum + emp.salarioTotalMensual, 0);
  csv += `\nTOTALES,,,${totalSemanal.toFixed(2)},${totalMensual.toFixed(2)}\n`;

  // Crear blob y descargar
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  
  link.setAttribute('href', url);
  link.setAttribute('download', `planilla_${new Date().toISOString().split('T')[0]}.csv`);
  link.style.visibility = 'hidden';
  
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// ==============================
// Event Listeners
// ==============================
document.addEventListener('DOMContentLoaded', function() {
  // Botón calcular
  document.getElementById('btnCalcular').addEventListener('click', calcularPlanilla);

  // Botón agregar a planilla
  document.getElementById('btnAgregarPlanilla').addEventListener('click', agregarAPlanilla);

  // Botón ver/ocultar planilla
  document.getElementById('btnVerPlanilla').addEventListener('click', function() {
    const tabla = document.getElementById('tablaPlanillaCompleta');
    if (tabla.style.display === 'none') {
      tabla.style.display = 'block';
      this.textContent = '📋 Ocultar Planilla';
    } else {
      tabla.style.display = 'none';
      this.textContent = '📋 Ver Planilla Completa';
    }
  });

  // Enter para calcular
  document.getElementById('formPlanilla').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      calcularPlanilla();
    }
  });
});