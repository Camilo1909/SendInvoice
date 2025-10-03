$(document).ready(function() {
       
    // Opcional: agregar efectos adicionales
    $('.sidebar-item').on('click', function() {
        $('.sidebar-item').removeClass('active');
        $(this).addClass('active');
    });
});