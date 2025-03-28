$(document).ready(function() {
    const bookId = $('#edit-book-form').data('book-id');
    
    // Initialize dialog
    $("#confirm-dialog").dialog({
        autoOpen: false,
        modal: true,
        buttons: {
            "Yes, discard changes": function() {
                $(this).dialog("close");
                // Redirect back to view page
                window.location.href = `/view/${bookId}`;
            },
            "No, continue editing": function() {
                $(this).dialog("close");
            }
        }
    });
    
    // Discard button handler
    $('#discard-button').on('click', function(e) {
        e.preventDefault();
        $("#confirm-dialog").dialog("open");
    });
    
    // Form validation and submission
    $('#edit-book-form').on('submit', function(e) {
        e.preventDefault();
        
        // Clear previous error messages
        $('.error-feedback').text('');
        
        // Validate form data
        let isValid = true;
        
        // Title validation
        const title = $('#title').val().trim();
        if (!title) {
            $('#title-error').text('Title is required');
            isValid = false;
        }
        
        // Author validation
        const author = $('#author').val().trim();
        if (!author) {
            $('#author-error').text('Author is required');
            isValid = false;
        }
        
        // Year validation
        const year = $('#year').val().trim();
        if (!year) {
            $('#year-error').text('Year is required');
            isValid = false;
        } else if (!/^\d{4}$/.test(year)) {
            $('#year-error').text('Please enter a valid 4-digit year');
            isValid = false;
        }
        
        // Rating validation
        const rating = $('#rating').val().trim();
        if (!rating) {
            $('#rating-error').text('Rating is required');
            isValid = false;
        } else if (isNaN(rating) || parseFloat(rating) < 0 || parseFloat(rating) > 5) {
            $('#rating-error').text('Rating must be a number between 0 and 5');
            isValid = false;
        }
        
        // Description validation
        const description = $('#description').val().trim();
        if (!description) {
            $('#description-error').text('Description is required');
            isValid = false;
        }
        
        // Image URL validation
        const image = $('#image').val().trim();
        if (!image) {
            $('#image-error').text('Image URL is required');
            isValid = false;
        } else if (!image.match(/^https?:\/\/.+\..+/)) {
            $('#image-error').text('Please enter a valid URL starting with http:// or https://');
            isValid = false;
        }
        
        // Process similar books (optional)
        let similar_novel_ids = [];
        const similarBooks = $('#similar_books').val().trim();
        if (similarBooks) {
            similar_novel_ids = similarBooks.split(',').map(id => id.trim());
        }
        
        // If all validations pass, submit the form via AJAX
        if (isValid) {
            const bookData = {
                title: title,
                author: author,
                year: year,
                rating: rating,
                description: description,
                image: image,
                similar_novel_ids: similar_novel_ids
            };
            
            // Submit data via AJAX
            $.ajax({
                url: `/api/books/${bookId}`,
                method: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify(bookData),
                success: function(response) {
                    // Redirect to the view page
                    window.location.href = `/view/${bookId}`;
                },
                error: function(xhr) {
                    // Handle errors
                    const response = xhr.responseJSON;
                    if (response && response.error) {
                        alert(`Error: ${response.error}`);
                    } else {
                        alert('An error occurred while updating the book. Please try again.');
                    }
                }
            });
        }
    });
});