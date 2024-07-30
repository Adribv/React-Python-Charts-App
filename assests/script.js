document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.dropdown-with-checkboxes').forEach(function(dropdown) {
        dropdown.addEventListener('click', function() {
            this.querySelector('.dropdown-options').classList.toggle('show');
        });
    });

    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown-with-checkboxes')) {
            document.querySelectorAll('.dropdown-options').forEach(function(options) {
                options.classList.remove('show');
            });
        }
    });
});
