function generatePDFWithFilters() {
    var fechaFiltro = document.querySelector('[name="fecha_filtro"]').value;
    var inspectorFiltro = document.querySelector('[name="inspector_filtro"]').value;

    var filters = {
        fecha: fechaFiltro,
        inspector: inspectorFiltro
    };

    var headerConfig = {
        title: "Reporte Personalizado",
        html: `
            <div class="header">
                <img src="/static/logo4.PNG" alt="Logo" />
                <div>
                    <h1>MI EMPRESA S.A.</h1>
                    <h4><p style="font-size: 20px; margin-top: 10px; text-align: center;">REPORTE ESPECIAL</p></h4>
                </div>
                <img src="/static/logo4.PNG" alt="Logo" />
            </div>
        `
    };

    generatePDF('.table', filters, headerConfig);
}