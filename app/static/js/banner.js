
    document.addEventListener('DOMContentLoaded', function () {
        var closeButtons = document.querySelectorAll('.btn-close');

        closeButtons.forEach(function (button) {
            button.addEventListener('click', function () {
                button.closest('.alert').remove();
            });
        });
    });