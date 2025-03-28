from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

books_data = {
    "1": {
        "id": "1",
        "title": "Hitchhiker's Guide to the Galaxy",
        "image": "https://m.media-amazon.com/images/I/71OPafHmyQL.jpg",
        "year": "1979",
        "description": "The Hitchhiker's Guide to the Galaxy by Douglas Adams is a wildly absurd sci-fi comedy that follows Arthur Dent, an ordinary Englishman who narrowly escapes Earth's destruction when it's demolished to make way for an intergalactic highway. Rescued by his eccentric friend Ford Prefect, a researcher for The Hitchhiker's Guide to the Galaxy, Arthur embarks on a chaotic journey through space, encountering a depressed robot, a two-headed galactic president, and the ultimate question to life, the universe, and everything. Along the way, he learns that the universe is vast, baffling, and deeply, hilariously indifferent to human concerns. Packed with sharp satire, surreal humor, and unforgettable characters, it's a must-read for anyone who enjoys sci-fi with a heavy dose of absurdity.",
        "author": "Douglas Adams",
        "rating": "3.8",
        "similar_novel_ids": ["5", "2", "3"]
    },
    "2": {
        "id": "2",
        "title": "Good Omens",
        "image": "https://prodimage.images-bn.com/pimages/9780060853976_p0_v12_s1200x630.jpg",
        "year": "1990",
        "description": "Good Omens by Neil Gaiman and Terry Pratchett is a comedic fantasy about an angel, Aziraphale, and a demon, Crowley, who have grown rather fond of Earth and secretly work together to prevent the apocalypse. Their plan hits a snag when they realize the Antichrist has been misplaced, leading to a mix-up involving an ordinary English boy who unknowingly holds the fate of the world in his hands. Meanwhile, a modern-day witch, a hapless witchfinder, and the Four Horsemen of the Apocalypse all play their parts in the impending end times. Filled with witty satire, absurd twists, and a surprisingly heartfelt look at good, evil, and free will, the novel is a wildly entertaining ride.",
        "author": "Terry Pratchett & Neil Gaiman",
        "rating": "4.2",
        "similar_novel_ids": ["1", "3", "4"]
    },
    "3": {
        "id": "3",
        "title": "Cat's Cradle",
        "image": "https://m.media-amazon.com/images/I/71m3P2Eie2L.jpg",
        "year": "2018",
        "description": "Cat's Cradle by Kurt Vonnegut is a darkly satirical novel that explores themes of science, religion, and human folly. The story follows a journalist researching the creator of the atomic bomb, only to uncover a deadly substance called ice-nine, capable of freezing all water on Earth. His journey leads him to the fictional island of San Lorenzo, where he encounters an absurd dictatorship and a bizarre religion called Bokononism, which embraces lies as a means to cope with life's meaninglessness. Blending humor with existential dread, the novel critiques blind faith in both science and ideology, making it a sharp, thought-provoking read.",
        "author": "Kurt Vonnegut",
        "rating": "4.2",
        "similar_novel_ids": ["1", "2", "4"]
    },
    "4": {
        "id": "4",
        "title": "Slaughterhouse-Five",
        "image": "https://m.media-amazon.com/images/I/817dhIc6E+L.jpg",
        "year": "1969",
        "description": "Slaughterhouse-Five by Kurt Vonnegut is a surreal, anti-war novel that follows Billy Pilgrim, a soldier who survives the firebombing of Dresden and becomes 'unstuck in time.' Jumping between moments in his life—his time as a prisoner of war, his mundane post-war existence, and even his supposed abduction by aliens—Billy passively experiences events without control or emotion. The novel blends dark humor, science fiction, and brutal realism to explore the absurdity of war and the illusion of free will. With its famous refrain, 'So it goes,' Vonnegut delivers a haunting yet strangely comic meditation on fate, trauma, and the human condition.",
        "author": "Kurt Vonnegut",
        "rating": "4.3",
        "similar_novel_ids": ["2", "3", "5"]
    },
    "5": {
        "id": "5",
        "title": "Red Shirts",
        "image": "https://m.media-amazon.com/images/I/919vMsBlMQL._AC_UF1000,1000_QL80_.jpg",
        "year": "2012",
        "description": "Redshirts by John Scalzi is a meta-science fiction novel that follows low-ranking crew members aboard the starship Intrepid, who begin to notice a disturbing pattern—junior officers on away missions tend to die at an alarming rate. As they investigate, they uncover a bizarre truth: their reality is being manipulated by the narrative logic of a poorly written TV show from another universe. Determined to escape their fate, they set out on a mind-bending mission to rewrite their own story. Packed with humor, self-aware genre satire, and surprising emotional depth, Redshirts is both a loving parody and a thoughtful exploration of storytelling itself.",
        "author": "John Scalzi",
        "rating": "4.0",
        "similar_novel_ids": ["1", "3", "4"]
    }
}

# Function to get popular items (first 3 in this case)
def get_popular_items():
    return [books_data[str(i)] for i in range(1, 4)]

@app.route('/')
def home():
    popular_items = get_popular_items()
    return render_template('home.html', popular_items=popular_items)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip().lower()
    
    if not query:
        return render_template('search_results.html', results=[], query="", count=0)
    
    results = []
    for book in books_data.values():
        # Check if query is in title, author, or description (case insensitive)
        if (query in book['title'].lower() or 
            query in book['author'].lower() or 
            query in book['description'].lower()):
            
            # Create a copy of the book with highlighted matches
            book_copy = book.copy()
            
            # Add matching fields to help with highlighting
            book_copy['matches'] = {
                'title': query in book['title'].lower(),
                'author': query in book['author'].lower(),
                'description': query in book['description'].lower()
            }
            
            results.append(book_copy)
    
    count = len(results)
    return render_template('search_results.html', results=results, query=query, count=count)

@app.route('/view/<book_id>')
def view_book(book_id):
    book = books_data.get(book_id)
    if book:
        # Get similar books based on similar_novel_ids
        similar_books = [books_data[similar_id] for similar_id in book.get('similar_novel_ids', [])]
        return render_template('book_view.html', book=book, similar_books=similar_books)
    return "Book not found", 404

@app.route('/add', methods=['GET'])
def add_book_page():
    return render_template('add_book.html')

# Add this route for handling the AJAX submission
@app.route('/api/books', methods=['POST'])
def add_book():
    # Get data from request
    data = request.json
    
    # Validate required fields
    required_fields = ['title', 'author', 'year', 'description', 'image', 'rating']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"success": False, "error": f"Missing required field: {field}"}), 400
    
    # Generate a new ID (use the next number after the highest existing ID)
    new_id = str(max([int(key) for key in books_data.keys()]) + 1)
    
    # Create new book entry
    new_book = {
        "id": new_id,
        "title": data['title'],
        "author": data['author'],
        "year": data['year'],
        "description": data['description'],
        "image": data['image'],
        "rating": data['rating'],
        "similar_novel_ids": data.get('similar_novel_ids', [])  # Optional field with default
    }
    
    # Add to books_data dictionary
    books_data[new_id] = new_book
    
    # Return success response with the new book ID
    return jsonify({"success": True, "id": new_id}), 201


@app.route('/edit/<book_id>', methods=['GET'])
def edit_book_page(book_id):
    book = books_data.get(book_id)
    if book:
        return render_template('edit_book.html', book=book)
    return "Book not found", 404

@app.route('/api/books/<book_id>', methods=['PUT'])
def update_book(book_id):
    # Check if book exists
    if book_id not in books_data:
        return jsonify({"success": False, "error": "Book not found"}), 404
    
    # Get data from request
    data = request.json
    
    # Validate required fields
    required_fields = ['title', 'author', 'year', 'description', 'image', 'rating']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"success": False, "error": f"Missing required field: {field}"}), 400
    
    # Update book data
    books_data[book_id].update({
        "title": data['title'],
        "author": data['author'],
        "year": data['year'],
        "description": data['description'],
        "image": data['image'],
        "rating": data['rating'],
        "similar_novel_ids": data.get('similar_novel_ids', [])
    })
    
    # Return success response
    return jsonify({"success": True}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)