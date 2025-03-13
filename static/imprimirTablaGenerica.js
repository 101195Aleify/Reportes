function imprimirTablaGenerica(tableSelector, filtersConfig, tituloReporte) {
    // Obtener la tabla objetivo
    var tablaOriginal = document.querySelector(tableSelector);
    if (!tablaOriginal) {
        console.error("No se encontró la tabla con el selector:", tableSelector);
        alert("Error: No se encontró la tabla para imprimir.");
        return;
    }

    // Clonar la tabla para modificarla sin afectar la vista
    var tablaClonada = tablaOriginal.cloneNode(true);
    var filas = tablaClonada.querySelectorAll('tr');
    var encabezado = filas[0].querySelectorAll('th');
    var indiceAcciones = -1; // Índice de la columna "Acciones" (si existe)

    // Identificar la columna "Acciones" en el encabezado
    encabezado.forEach((th, index) => {
        if (th.textContent.trim().toLowerCase() === 'acciones') {
            indiceAcciones = index;
        }
    });

    // Iterar sobre las filas para aplicar filtros y eliminar la columna "Acciones"
    filas.forEach(function(fila, index) {
        if (index === 0 && indiceAcciones !== -1) {
            // Eliminar la columna "Acciones" del encabezado
            fila.deleteCell(indiceAcciones);
            return;
        }
        if (index > 0) { // Filas de datos
            var celdas = fila.querySelectorAll('td');
            var debeMostrar = true;

            // Aplicar filtros si se proporcionan
            if (filtersConfig) {
                for (var filterKey in filtersConfig) {
                    var filterValue = document.querySelector(`[name="${filterKey}"]`).value;
                    if (filterValue) {
                        var cellValue = celdas[filtersConfig[filterKey].index].innerText.trim();
                        if (cellValue !== filterValue) {
                            debeMostrar = false;
                            break;
                        }
                    }
                }
            }

            if (!debeMostrar) {
                fila.remove();
            } else if (indiceAcciones !== -1) {
                // Eliminar la columna "Acciones" de las filas de datos
                fila.deleteCell(indiceAcciones);
            }
        }
    });

    // Definir los estilos para la impresión
    var estilos = `
        <style>
            body {
                font-family: 'Arial', sans-serif;
                margin: 20mm;
                background-color: #f5f5f5;
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
            }
            .header img {
                max-width: 150px;
                height: auto;
            }
            .table {
                table-layout: fixed;
                width: 100%;
                border-collapse: collapse;
                background: #ffffff;
                font-size: 8px;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            }
            .table th, .table td {
                padding: 8px;
                border: 4px solid #ddd;
                text-align: center;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            .table th {
                background: #004080;
                color: #ffffff;
                font-weight: bold;
                height: 40px;
            }
            .table td {
                height: 30px;
            }
            .vertical-text {
                writing-mode: vertical-rl;
                transform: rotate(180deg);
                text-align: center;
                padding: 5px;
                font-size: 11px;
                line-height: 1.2;
                font-weight: bold;
                color: #ffffff;
                background-color: #0066cc;
                border-bottom: 2px solid #003366;
                overflow: hidden;
            }
            th.vertical-text {
                width: 30px;
                height: 120px;
                vertical-align: bottom;
                word-wrap: break-word;
            }
            .table th:nth-child(12), .table td:nth-child(12) {
                width: 50px;
            }
            .table th:not(.vertical-text) {
                width: 80px;
            }
            .table td:not(.vertical-text) {
                width: 80px;
            }
            .table th:nth-child(13), .table td:nth-child(13) {
                width: 150px;
            }
            .table tr:nth-child(even) {
                background: #f2f2f2;
            }
            @media print {
                .no-print { display: none; }
                body { margin: 0; background: #ffffff; }
                .table th {
                    background: #004080 !important;
                    color: #ffffff !important;
                }
                .vertical-text {
                    background-color: #0066cc !important;
                    color: #ffffff !important;
                }
                img {
                    -webkit-print-color-adjust: exact;
                    print-color-adjust: exact;
                }
            }
        </style>
    `;

    // Crear una nueva ventana para la impresión
    var ventanaImpresion = window.open('', '', 'width=800,height=600');
    ventanaImpresion.document.write(`
        <html>
        <head>
            <title>Impresión de Reporte</title>
            ${estilos}
        </head>
        <body>
            <div class="header">
                <img src="/static/logo4.PNG" alt="Logo" />
                <div>
                    <h1>FRANK POR LABORATORIOS S.A DE C.V</h1>
                    <h4 style="font-size: 20px; margin-top: 10px; text-align: center;">${tituloReporte}</h4>
                </div>
                <img src="/static/logo4.PNG" alt="Logo" />
            </div>
            ${tablaClonada.outerHTML}
        </body>
        </html>
    `);
    ventanaImpresion.document.close();

    // Imprimir automáticamente después de cargar
    ventanaImpresion.onload = function() {
        ventanaImpresion.focus();
        ventanaImpresion.print();
        // ventanaImpresion.close(); // Descomenta si deseas cerrar la ventana después de imprimir
    };
}

// Ejemplo de uso para una tabla específica con filtros
function configurarImpresion() {
    var tableSelector = '.table'; // Selector de la tabla (puede ser personalizado)
    var filtersConfig = {
        'fecha_filtro': { index: 0 }, // Índice de la columna de fecha (ajusta según tu tabla)
        'inspector_filtro': { index: 1 } // Índice de la columna de inspector (ajusta según tu tabla)
    };

    // Asignar la función al botón de impresión
    document.querySelector('button[onclick="imprimirTabla()"]')?.addEventListener('click', function() {
        imprimirTablaGenerica(tableSelector, filtersConfig, "REVISIÓN DEL ÁREA (FABRICACIÓN, AP1, AP2, AP3)");
    });
}

// Llamar a la configuración al cargar la página
window.onload = function() {
    configurarImpresion();
    // Otra lógica de inicialización (como actualizar hora) puede ir aquí
};