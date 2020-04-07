class User:

    counter = 1

    def __init__(self, name, password):

        # Keep track of id number.
        self.id = User.counter
        User.counter += 1

        # Details about user.
        self.name = name
        self.password = password
 

class Book:

    def __init__(self, isbn, title, author, year);

        #Details about book.
        self.isbn=isbn
        self.title=title
        self.author=author
        self.year=year


class Review:

    counter = 1

    def __init__(self, username, isbn, mark, text)
      
        # Keep track of id number.
        self.id = User.counter
        User.counter += 1

        #Details about review.
        self.username=username
        self.isbn=isbn
        self.mark=mark
        self.text=text