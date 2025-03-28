$(document).ready(function() {
    const query = document.getElementById('search-results').dataset.query;
    
    if (query) {
        // Function to highlight matches
        function highlightText(element, shouldHighlight) {
            if (shouldHighlight === "True") {
                const text = element.text();
                const regex = new RegExp(query, 'gi');
                const highlightedText = text.replace(regex, match => 
                    `<span class="highlight">${match}</span>`);
                element.html(highlightedText);
            }
        }
        
        // Apply highlighting
        $('.search-title').each(function() {
            highlightText($(this), $(this).data('match'));
        });
        
        $('.search-author').each(function() {
            highlightText($(this), $(this).data('match'));
        });
        
        $('.search-desc').each(function() {
            highlightText($(this), $(this).data('match'));
        });
    }
});