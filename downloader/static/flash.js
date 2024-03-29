document.querySelectorAll('.flash-button').forEach(function(button) {
    button.addEventListener('click', function() {
        this.parentElement.style.display = 'none';
    });
});

$('.flash-button').click(function() {
    $(this).parent().hide();
});