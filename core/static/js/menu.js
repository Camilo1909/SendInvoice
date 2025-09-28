$(document).ready(function() {
    $('#menu-toggle').click(function() {
        $('#menu-items').toggleClass('show'); // Muestra/oculta menú
        const icon = $('#menu-icon');
        icon.text(icon.text() === '☰' ? '✕' : '☰'); // Cambia icono
    });
});
