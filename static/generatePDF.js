// pdfGenerator.js

function generatePDF(tableSelector, filters = {}, headerConfig = {}) {
    // Obtener la tabla original
    var tablaOriginal = document.querySelector(tableSelector);
    if (!tablaOriginal) {
        console.error("No se encontró la tabla con el selector:", tableSelector);
        return;
    }

    // Clonar la tabla para modificarla sin afectar la original
    var tablaClonada = tablaOriginal.cloneNode(true);
    var filas = tablaClonada.querySelectorAll('tr');

    // Aplicar filtros si se proporcionan
    filas.forEach(function(fila, index) {
        if (index === 0) {
            // Eliminar la columna "Acciones" del encabezado (si existe)
            if (fila.cells[fila.cells.length - 1].innerText === "Acciones") {
                fila.deleteCell(-1);
            }
            return;
        }

        var fecha = fila.cells[0].innerText;
        var inspector = fila.cells[12] ? fila.cells[12].innerText : ""; // Ajustar según la tabla

        // Filtrar filas según los filtros proporcionados
        if ((filters.fecha && fecha !== filters.fecha) || 
            (filters.inspector && inspector !== filters.inspector)) {
            fila.remove();
        } else {
            // Eliminar la columna "Acciones" de las filas de datos (si existe)
            if (fila.cells[fila.cells.length - 1].innerText === "Eliminar" || 
                fila.cells[fila.cells.length - 1].querySelector('a')) {
                fila.deleteCell(-1);
            }
        }
    });

    // Estilos CSS para el PDF
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
            }
            th.vertical-text {
                width: 30px;
                height: 120px;
                vertical-align: bottom;
            }
            .table th:not(.vertical-text) { width: 80px; }
            .table td:not(.vertical-text) { width: 80px; }
            .table th:nth-child(13), .table td:nth-child(13) { width: 50px; }
            .table th:nth-child(14), .table td:nth-child(14) { width: 150px; }
            .table tr:nth-child(even) { background: #f2f2f2; }
            @media print {
                .no-print { display: none; }
                body { margin: 0; background: #ffffff; }
                .table th { background: #004080 !important; color: #ffffff !important; }
                .vertical-text { background-color: #0066cc !important; color: #ffffff !important; }
            }
        </style>
    `;

    // Configuración del encabezado por defecto o personalizado
    var defaultHeader = `
        <div class="header">
            <img src="/static/logo4.PNG" alt="Logo" />
            <div>
                <h1>FRANK POR LABORATORIOS S.A DE C.V</h1>
                <h4><p style="font-size: 20px; margin-top: 10px; text-align: center;">REVISIÓN DE LINEA DE ENVASADO</p></h4>
            </div>
            <img src="/static/logo4.PNG" alt="Logo" />
        </div>
    `;
    var headerHTML = headerConfig.html || defaultHeader;

    // Crear la ventana de impresión
    var ventanaImpresion = window.open('', '', 'width=800,height=600');
    ventanaImpresion.document.write(`
        <html>
        <head>
            <title>${headerConfig.title || 'Registro de Nuevo Reporte de Calidad'}</title>
            ${estilos}
        </head>
        <body>
            ${headerHTML}
            ${tablaClonada.outerHTML}
        </body>
        </html>
    `);
    ventanaImpresion.document.close();

    // Imprimir automáticamente
    ventanaImpresion.onload = function() {
        ventanaImpresion.focus();
        ventanaImpresion.print();
        // ventanaImpresion.close(); // Descomentar si deseas cerrar la ventana tras imprimir
    };
}