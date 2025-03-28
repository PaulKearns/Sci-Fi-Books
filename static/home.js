// jQuery document ready function
$(document).ready(function() {
    // Get the container for popular books
    const popularBooksContainer = $('#popular-books');
    
    // Check if popularBooks variable exists (passed from the HTML)
    if (typeof popularBooks !== 'undefined' && popularBooksContainer.length) {
        // Iterate through each book and create cards
        popularBooks.forEach(book => {
            const bookCard = `
                <div class="col-md-4 mb-4">
                    <div class="card book-card">
                        <div class="position-relative">
                            <a href="/view/${book.id}">
                                <img src="${book.image}" alt="${book.title} book cover" class="book-cover-preview">
                            </a>
                        </div>
                        <div class="book-info">
                            <h5 class="card-title dark-grey">${book.title}</h5>
                            <p class="card-text light-grey">By ${book.author}</p>
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <span class="accent-color fs-5">${book.rating}/5 <i class="bi bi-star-fill"></i></span>
                            </div>
                            <a href="/view/${book.id}" class="btn btn-primary w-100">
                                <i class="bi bi-book me-2"></i>View Details
                            </a>
                        </div>
                    </div>
                </div>
            `;
            // Append using jQuery
            popularBooksContainer.append(bookCard);
        });
    } else {
        console.error('Popular books data not found or container not found');
    }
});