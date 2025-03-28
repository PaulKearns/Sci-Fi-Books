$(document).ready(function() {
    // Search form submission
    $('#search-form').on('submit', function(e) {
        e.preventDefault();
        const searchQuery = $('#search-input').val().trim();
        
        if (searchQuery === '') {
            $('#search-input').val('').focus();
            return;
        }

        window.location.href = `/search?query=${encodeURIComponent(searchQuery)}`;
    });

    // Add active class to current nav item
    const path = window.location.pathname;
    if (path === '/') {
        $('.navbar-nav .nav-link').eq(0).addClass('active');
    } else if (path.includes('/add')) {
        $('.navbar-nav .nav-link').eq(1).addClass('active');
    }
});