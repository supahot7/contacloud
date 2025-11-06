// static/js/planilla.js - Corregido
document.addEventListener('DOMContentLoaded', function() {
    const btnCalcular = document.getElementById('btnCalcular');
    const btnAgregar = document.getElementById('btnAgregarPlanilla');
    const btnVerPlanilla = document.getElementById('btnVerPlanilla');
    
    if (btnCalcular) {
        btnCalcular.addEventListener('click', calcularPlanilla);
    }
    
    if (btnAgregar) {
        btnAgregar.addEventListener('click', agregarAPlanilla);
    }
    
    if (btnVerPlanilla) {
        btnVerPlanilla.addEventListener('click', toggleTablaPlanilla);
    }
    
    // Calcular automáticamente cuando cambien los valores
    const inputsCalculo = ['salario_nominal', 'dias_trabajados'];
    inputsCalculo.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.addEventListener('input', calcularPlanilla);
        }
    });
    
    // También calcular cuando cambie la antigüedad
    const radiosAntiguedad = document.querySelectorAll('input[name="anos_trabajados"]');
    radiosAntiguedad.forEach(radio => {
        radio.addEventListener('change', calcularPlanilla);
    });
});

function calcularPlanilla() {
    const salarioNominal = parseFloat(document.getElementById('salario_nominal').value) || 0;
    const anosTrabajados = document.querySelector('input[name="anos_trabajados"]:checked').value;
    const diasTrabajados = parseInt(document.getElementById('dias_trabajados').value) || 30; // ✅ OBTENER DÍAS TRABAJADOS
    
    if (salarioNominal <= 0) {
        resetearResultados();
        return;
    }
    
    // Validar días trabajados
    if (diasTrabajados <= 0 || diasTrabajados > 31) {
        alert('Los días trabajados deben estar entre 1 y 31');
        resetearResultados();
        return;
    }
    
    // Llamada AJAX para cálculo en tiempo real
    fetch('/costos/planilla/calcular-ajax/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCSRFToken()
        },
        body: `salario_nominal=${salarioNominal}&anos_trabajados=${anosTrabajados}&dias_trabajados=${diasTrabajados}` // ✅ INCLUIR DÍAS TRABAJADOS
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            actualizarResultados(data);
        } else {
            console.error('Error en cálculo:', data.error);
            resetearResultados();
            alert('Error en el cálculo: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        resetearResultados();
        alert('Error de conexión al calcular la planilla');
    });
}

function actualizarResultados(data) {
    document.getElementById('res_sueldo_nominal').textContent = `$${data.sueldo_nominal.toFixed(2)}`;
    document.getElementById('res_costo_semana').textContent = `$${data.costo_semana.toFixed(2)}`;
    document.getElementById('res_septimo').textContent = `$${data.septimo.toFixed(2)}`;
    document.getElementById('res_vacaciones').textContent = `$${data.vacaciones.toFixed(2)}`;
    document.getElementById('res_aguinaldo').textContent = `$${data.aguinaldo.toFixed(2)}`;
    document.getElementById('res_salario_cancelado').textContent = `$${data.salario_cancelado.toFixed(2)}`;
    document.getElementById('res_isss').textContent = `$${data.isss.toFixed(2)}`;
    document.getElementById('res_afp').textContent = `$${data.afp.toFixed(2)}`;
    document.getElementById('res_incaf').textContent = `$${data.incaf.toFixed(2)}`;
    document.getElementById('res_total_semanal').textContent = `$${data.total_semanal.toFixed(2)}`;
    document.getElementById('res_total_mensual').textContent = `$${data.total_mensual.toFixed(2)}`;
}

function resetearResultados() {
    const resultados = document.querySelectorAll('.resultado-value');
    resultados.forEach(resultado => {
        resultado.textContent = '$0.00';
    });
}

function getCSRFToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfToken) {
        return csrfToken.value;
    }
    return '';
}

function agregarAPlanilla() {
    // Validar formulario antes de enviar
    const salarioNominal = parseFloat(document.getElementById('salario_nominal').value) || 0;
    const diasTrabajados = parseInt(document.getElementById('dias_trabajados').value) || 30;
    
    if (salarioNominal <= 0) {
        alert('Por favor ingrese un salario nominal válido');
        return;
    }
    
    if (diasTrabajados <= 0 || diasTrabajados > 31) {
        alert('Los días trabajados deben estar entre 1 y 31');
        return;
    }
    
    document.getElementById('formPlanilla').submit();
}

function toggleTablaPlanilla() {
    const tabla = document.getElementById('tablaPlanillaCompleta');
    if (tabla) {
        tabla.style.display = tabla.style.display === 'none' ? 'block' : 'none';
        
        // Cambiar el texto del botón
        const btnVerPlanilla = document.getElementById('btnVerPlanilla');
        if (btnVerPlanilla) {
            if (tabla.style.display === 'none') {
                btnVerPlanilla.textContent = '📋 Ver Planilla Completa';
            } else {
                btnVerPlanilla.textContent = '👁️ Ocultar Planilla';
            }
        }
    }
}

// Función adicional para formatear números
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2
    }).format(amount);
}

// Calcular automáticamente al cargar la página si hay valores
document.addEventListener('DOMContentLoaded', function() {
    // Esperar un momento para que los elementos se carguen completamente
    setTimeout(() => {
        const salarioNominal = parseFloat(document.getElementById('salario_nominal').value) || 0;
        if (salarioNominal > 0) {
            calcularPlanilla();
        }
    }, 500);
});