import csv
from datetime import datetime
from typing import List, Dict

# global variable for active book collection
active_books = []


# Function to load books from a CSV file
def load_books(filename: str):
    # Check if the file exists, if not, show an error message
    # Load books from the CSV file and populate the active_books list
    existing_book_ids = list(book['bookID'] for book in active_books)
    try:
        with open(filename, 'r', newline='', encoding='utf-8', errors='replace') as csvfile:
            reader = csv.DictReader(csvfile)
            # active_books.clear()
            for row in reader:
                if row['bookID'] not in existing_book_ids:
                    active_books.append(row)

        print(f"Books have been loaded from {filename}")
    except FileNotFoundError:
        print(f"The specified file '{filename}' does not exist.")


# Function to format the output into tabular format
def format_table(books):
    # Define headers for the table
    headers = ["bookID", "title", "authors", "average_rating",
               "language_code", "num_pages", "publication_date", "publisher"]
    # Calculate initial column widths based on header lengths
    column_widths = {header: len(header) for header in headers}
    # Create a format string for proper alignment in the table
    format_string = " | " .join('{{:<{}}}'.format(
        width + 2) for width in column_widths.values())
    # Update column widths based on the maximum width of data in each column
    for header in headers:
        max_wid = max(len(str(book[header])) for book in books)
        if max_wid > column_widths[header]:
            column_widths[header] = max_wid
        format_string = " | " .join('{{:<{}}}'.format(
            width) for width in column_widths.values())

    # Create and print the header row along with a divider
    header_row = format_string.format(*headers)
    divider = '-' * len(header_row)
    print(header_row)
    print(divider)
    # Print each row of data in the formatted table
    for book in books:
        print(format_string.format(
            *[str(book[header]) for header in headers]))

# Function to list all books in the active book collection


def list_books(input_books):
    org_books = clean_column_headers(input_books)
    batch = 10
    column_widths = {}
    # headers = list(active_books[0].keys())
    headers = ["bookID", "title", "authors", "average_rating",
               "language_code", "num_pages", "publication_date", "publisher"]
    column_widths = {header: len(header) for header in headers}
    format_string = " | " .join('{{:<{}}}'.format(
        width + 2) for width in column_widths.values())
    if len(org_books) == 0:
        header_row = format_string.format(*headers)
        divider = '-' * len(header_row)
        print(header_row)
        print(divider)
        print()
        print("The active book collection is empty.")
    else:
        if len(org_books) > batch:
            print(
                "The active books collection is large. So, the program will print out the first 10 lines!")
            while True:
                books = org_books[:batch]
                org_books = org_books[batch:]
                format_table(books)
                inp = input("Continue printing(y/n): ")
                if inp != "y":
                    break
        else:
            format_table(org_books)

# Function to show information of a specific book


def show_book_info():
    # Loop to continuously prompt the user for book ID or ISBN13
    while True:
        # Get user input for book ID or ISBN13
        userIn = input("Enter the book ID or ISBN13:\n")

        # Iterate through the active_books to find the specified book
        for book in active_books:
            # Check if the bookID or ISBN13 matches the user input
            if book.get('bookID') == userIn or book.get('isbn13') == userIn:
                # Print detailed information about the found book
                print(f"Title: {book.get('title')}")
                print(f"Authors: {book.get('authors')}")
                print(f"Average Rating: {book.get('average_rating')}")
                print(f"ISBN: {book.get('isbn')}")
                print(f"ISBN13: {book.get('isbn13')}")
                print(f"Language Code: {book.get('language_code')}")
                print(f"Number of Pages: {book.get('  num_pages')}")
                print(f"Ratings Count: {book.get('ratings_count')}")
                print(f"Text Reviews Count: {book.get('text_reviews_count')}")
                print(f"Publication Date: {book.get('publication_date')}")
                print(f"Publisher: {book.get('publisher')}")
                break  # Exit the loop once the book is found
        else:
            # If the loop completes without finding the book, print a message based on input length
            if len(userIn) == 13:
                print(f"ISBN13: {userIn} not found.")
            else:
                print(f"BookID: {userIn} not found.")

        # Ask the user if they want to continue viewing specific book information
        inp = input(
            "Would you like to continue viewing the specific book information(y/n)?: ").lower()
        if inp != "y":
            break  # Exit the loop if the user doesn't want to continue


# Function to insert a book into the active book collection
def insert_book():
    # Get a list of existing book IDs to check for duplicates
    existing_book_ids = list(book['bookID'] for book in active_books)

    while True:
        # Create an empty dictionary to store information about the new book
        new_book = {}
        # Define the fields that need to be filled for the new book
        fields = [
            'bookID', 'title', 'authors', 'average_rating', 'isbn', 'isbn13',
            'language_code', 'num_pages', 'ratings_count', 'text_reviews_count',
            'publication_date', 'publisher'
        ]

        # Prompt the user to input values for each field
        print("Enter -1 to stop")
        for field in fields:
            # Continuously prompt the user until a non-empty value is provided
            while True:
                value = input(f"Input {field}: ")

                if len(value) > 0:
                    break
                else:
                    print("Value cannot be None!")

            # Check if the user wants to cancel the operation
            if value == "-1":
                print('Cancelled')
                return
            else:
                # Check if the entered bookID already exists in the active book collection
                if field == "bookID" and value in existing_book_ids:
                    print("BookId already exists!")
                    print("You can't add this book!")
                    break
                else:
                    # Add the field and its corresponding value to the new_book dictionary
                    new_book[field] = value

        # Append the new_book dictionary to the active_books list
        active_books.append(new_book)

        # Print a success message if the new book was added
        if len(new_book) > 0:
            print("Book added successfully.")

        # Ask the user if they want to continue inserting books
        print("Would you like to continue inserting books(y/n)")
        if input().lower() != "y":
            break  # Exit the loop if the user doesn't want to continue

# Function to delete books from the active book collection based on various criteria


def delete_book():
    while True:
        print("Choose a filter for deletion:")
        print("1. Delete by bookID")
        print("2. Delete by isbn13")
        print("3. Delete by average ratings")
        print("4. Delete by language code")
        print("5. Delete by publication date")
        print("6. Delete by Publisher")
        print("7. Delete by Author")
        print("8. Delete by Title")
        print("0. Back to Main Menu")
        print("x. Exit the program")
        choice = input("Enter your choice: ")
        books_to_remove = []
        if choice == "1":
            bookID = input("Enter the bookID to delete: ")
            for book in active_books:
                if book['bookID'] == bookID:
                    books_to_remove.append(book)
            if not books_to_remove:
                print("Input bookID is not found!")
        elif choice == "2":
            isbn13 = input("Enter the isbn13 to delete: ")
            for book in active_books:
                if book['isbn13'] == isbn13:
                    books_to_remove.append(book)
            if not books_to_remove:
                print("Input isbn13 is not found!")
        elif choice == "3":
            avg_rating = float(input("Enter the average rating: "))

            if avg_rating >= 0 and avg_rating <= 5:
                print(
                    "Delete books with ratings greater than or less than specified rating?: \n 0:greater than \n 1:less than")
                inp = input("Enter the choice: ")
                for book in active_books:
                    if inp == "0" and float(book['average_rating']) > avg_rating:
                        books_to_remove.append(book)
                    elif inp == "1" and float(book['average_rating']) < avg_rating:
                        books_to_remove.append(book)
            else:
                print("Input avg_rating is out of range!")
        elif choice == "4":
            lang_code = input(
                "Enter the language code to delete books of that language: ")
            for book in active_books:
                if book['language_code'] == lang_code:
                    books_to_remove.append(book)
            if not books_to_remove:
                print("Input language code is not found!")

        elif choice == "5":
            pub_date = input(
                "Enter the publication date (in M/D/YY format) to delete books of that date(Eg:9/5/2003): ")
            for book in active_books:
                if book['publication_date'] == pub_date:
                    books_to_remove.append(book)
            if not books_to_remove:
                print("Input publication date is not found!")
        elif choice == "6":

            publisher = input(
                "Enter the publisher name to delete books of that publisher: ")
            for book in active_books:
                if book['publisher'] == publisher:
                    books_to_remove.append(book)
            if not books_to_remove:
                print("Input publisher is not found!")
        elif choice == "7":
            author = input(
                "Enter the author name to delete books of that author: ")
            for book in active_books:
                if book['authors'] == author:
                    books_to_remove.append(book)
            if not books_to_remove:
                print("Input author is not found!")
        elif choice == "8":
            title = input("Enter the title to delete books of that title: ")
            for book in active_books:
                if book['title'] == title:
                    books_to_remove.append(book)
            if not books_to_remove:
                print("The input title is not found!")
        elif choice == "0":
            break
        elif choice == "x":
            exit()
        # Perform the deletion if books are to be removed
        if len(books_to_remove) > 0:
            # Print out the number of books to delete
            print(f"Number of books to delete: {len(books_to_remove)}")
            for book in books_to_remove:
                active_books.remove(book)
            print("Deleteion is completed")

        print("Would you like to continue deleting(y/n)")
        if input().lower() != "y":
            break

# Function to sort books in the active book collection


def clean_title(title):
    # Remove non alphabetic chars and convert to lowercase for title sorting.
    return ''.join(char.lower() for char in title if char.isalpha())


def convert_to_datetime(book):
    # Convert book's pub_date to a datetime object, handle invalid dates.
    try:
        return datetime.strptime(book['publication_date'], '%m/%d/%Y')
    except ValueError:
        return datetime.min


def filter_valid_dates(books):
    # Filter out books with invalid pub_dates.
    return [book for book in books if convert_to_datetime(book) != datetime.min]


def sort_books():
    # Sort a list of books based on sort key and order.
    global active_books
    while True:
        sort_num_key = {
            '1': 'bookID',
            '2': 'title',
            '3': 'average_rating',
            '4': '  num_pages',
            '5': 'publication_date'
        }
        sort_key = input(
            "Enter sorting group:\n\t 1. BookID\n\t 2. Title\n\t 3. Average Ratings\n\t 4. Number of pages\n\t 5. Publication Date\n\t Enter your choice: "
        )
        if sort_key not in sort_num_key:
            print("Invalid sort key entry.")
            break
        order = input(
            "Enter the order:\n\t 1. Ascending Order\n\t 2. Descending Order\n\t Enter your choice: "
        )
        if order not in ['1', '2']:
            print("Invalid order entry.")
            break

        active_books = filter_valid_dates(active_books)

        if sort_key in ['1', '3', '4']:
            active_books.sort(key=lambda x: float(x[sort_num_key[sort_key]]),
                              reverse=(order == '2'))
        elif sort_key == '2':
            active_books.sort(key=lambda x: clean_title(x['title']),
                              reverse=(order == '2'))
        elif sort_key == '5':
            active_books.sort(key=convert_to_datetime, reverse=(order == '2'))
        print("The books have been successfully sorted.")

        return active_books


# Function to search books based on user input
def search_books():
    while True:
        # Display menu options
        print('Choose the description.')
        print('1: Search by Title.')
        print('2: Search by Author.')
        print('3: Search by Title and Author.')
        print("0: Back to Main Menu")
        print("x: Exit the program")

        # Get user choice
        choice = input('Enter a choice: ').lower()
        book_to_search = []

        if choice == "1":
            # Search by Title
            search_title = input("Enter the Title to search: ").lower()

            for book in active_books:
                # Check if the search title matches or is a subset of the book title
                if search_title == book['title'].lower():
                    book_to_search.append(book)
                else:
                    title_list = book['title'].lower().split()
                    if all(x in title_list for x in search_title.split()):
                        book_to_search.append(book)

        elif choice == "2":
            # Search by Author
            search_author = input("Enter the author to search: ").lower()

            for book in active_books:
                # Check if the search author matches or is a subset of the book authors
                if search_author == book['authors'].lower():
                    book_to_search.append(book)
                else:
                    author_list = book['authors'].lower().split()
                    if all(x in author_list for x in search_author.split()):
                        book_to_search.append(book)

        elif choice == "3":
            # Search by Title and Author
            search_title = input("Enter the Title to search: ").lower()
            search_author = input("Enter the author to search: ").lower()
            # Check if both search title and search author match or are subsets of book title and authors
            for book in active_books:
                if search_title == book['title'].lower() and search_author == book['authors'].lower():
                    book_to_search.append(book)
                else:
                    title_list = book['title'].lower().split()
                    author_list = book['authors'].lower().split()
                    if all(x in title_list for x in search_title.split()) and all(x in author_list for x in search_author.split()):
                        book_to_search.append(book)
        elif choice == "0":
            # Go back to the main menu
            break
        elif choice == "x":
            # Exit the program
            exit()
        # Display the search results
        if len(book_to_search) == 0:
            print("Not found book!")
        else:
            list_books(book_to_search)

        # Ask if the user wants to continue searching
        print("Would you like to continue searching(y/n)")
        if input().lower() != "y":
            break


# Function to update information for a specific book in the active book collection
def update_books():
    while True:
        # Check if the book collection is empty
        if not active_books:
            print("The book collection is empty.")
        else:
            # Get the bookID from the user to identify the book for updating
            id = input("Enter the bookID of the book to modify: ")
            temp = {}

            # Get the headers (fields) of the books
            headers = [header for header in active_books[0].keys()]

            # Check if the provided bookID exists in the active book collection
            if id in list(book['bookID'] for book in active_books):
                print("Choose which part of the book to be updated:")

                # Display the available fields for updating
                for count, header in enumerate(headers):
                    print(f"\t {count}. {header}")
                    temp[str(count)] = header

                # Get user choice for the field to be updated
                choice = input("\t Enter your choice: ")
                key = temp[choice]

                # Find the book with the specified bookID
                for book in active_books:
                    if book["bookID"] == id:
                        current_book = book

                # Display the current value of the selected field for the book
                print(f"You're updating the field {key}.")
                print(
                    f"Current value of the {key} for this book is: {current_book[key]}")

                # Get user input for the updated value
                update_inp = input("Enter your updated value: ")

                # Update the selected field for the book
                for book in active_books:
                    if book["bookID"] == id:
                        book[key] = update_inp
                        update_book = [book]

                print("The book is updated!")
                print("The updated information of the book is:")
                list_books(update_book)
            else:
                print("The bookId is not found!")

        # Ask the user if they want to continue updating books
        inp = input("Would you like to continue updating(y/n)?: ").lower()
        if inp != "y":
            break


# Function to clean up the headers in the same format
def clean_column_headers(books=active_books):
    new_list = []
    for book in books:
        temp_a = {}
        for col, val in book.items():
            temp_a[col.strip().replace(' ', '_')] = val
        new_list.append(temp_a)
    return new_list

# Function to calculate statistical information about the active book collection


def calculate_statistics(books_list):

    num_books = len(books_list)
    if num_books > 0:
        books = clean_column_headers(books_list)

        authors, publishers, languages, years = ({}, {}, {}, {})
        reviews, ratings, pages = ([], [], [])
        for book in books:
            pages.append(int(book['num_pages']))
            ratings.append(float(book['average_rating']))
            reviews.append(int(book['text_reviews_count']))
            publishers[book['publisher']] = publishers.get(
                book['publisher'], 0)+1
            languages[book['language_code']] = languages.get(
                book['language_code'], 0)+1
            # date_object = datetime.strptime(book['publication_date'], "%m/%d/%Y") #Can't use datetime because there's some dates out of range 11/31/2000 and 6/31/1982
            # years[str(date_object.year)] = years.get(date_object.year, 0)+1
            year = book['publication_date'].split('/')[-1]
            years[year] = years.get(year, 0)+1
            authors[book['authors']] = authors.get(book['authors'], 0)+1
        num_distinct_authors = len(authors)
        total_pages = sum(pages)
        num_distinct_publishers = len(publishers)
        avg_books_per_year = num_books / len(years)
        num_languages = len(languages)

        avg_pages_per_book = total_pages / num_books

        avg_rating = sum(ratings) / num_books

        min_pages = min(pages)
        max_pages = max(pages)

        max_author, max_books_per_author = max(
            authors, key=authors.get), max(authors.values())
        min_author, min_books_per_author = min(
            authors, key=authors.get), min(authors.values())
        max_publisher, max_books_per_publisher = max(
            publishers, key=publishers.get), max(publishers.values())
        min_publisher, min_books_per_publisher = min(
            publishers, key=publishers.get), min(publishers.values())
        max_year, max_books_per_year = max(
            years, key=years.get), max(years.values())
        min_year, min_books_per_year = min(
            years, key=years.get), min(years.values())
        max_languages, max_books_per_languages = max(
            languages, key=languages.get), max(languages.values())
        min_languages, min_books_per_languages = min(
            languages, key=languages.get), min(languages.values())
        total_reviews_count = sum(
            int(book['text_reviews_count']) for book in books)

        print("\t\tStatistical Information:")
        print(f"\t-Number of Books: {num_books}")
        print()
        print(f"\t-Number of Distinct Authors: {num_distinct_authors}")
        print(
            f"\t-Books per Author (Max): {max_author} : {max_books_per_author} books")
        print(
            f"\t-Books per Author (Min): {min_author} : {min_books_per_author} books")
        print()

        print(f"\t-Number of Distinct Publishers: {num_distinct_publishers}")
        print(
            f"\t-Books per Publishers (Max): {max_publisher} : {max_books_per_publisher} books")
        print(
            f"\t-Books per Publishers (Min): {min_publisher} : {min_books_per_publisher} books")
        print()
        print(f"\t-Number of Distinct Language: {num_languages}")
        print(
            f"\t-Books per Language (Max): {max_languages} : {max_books_per_languages} books")
        print(
            f"\t-Books per Language (Min): {min_languages} : {min_books_per_languages} books")
        print()

        print(f"\t-Total Number of Pages from All Books: {total_pages}")
        print(f"\t-Minimum Pages: {min_pages}")
        print(f"\t-Maximum Pages: {max_pages}")
        print(f"\t-Average Number of Pages per Book: {avg_pages_per_book:.2f}")
        print()
        print(f"\t-Average Number of Books per Year: {avg_books_per_year:.2f}")
        print(
            f"\t-Books per Year (Max): {max_year} : {max_books_per_year} books")
        print(
            f"\t-Books per Year (Min): {min_year} : {min_books_per_year} books")
        print()
        print(f"\t-Average Rating: {avg_rating:.2f}")
        print(f"\t-Total Reviews Count: {total_reviews_count}")

    else:
        print("The active book collection is empty.")


# Function to save books to a CSV file
def save_books_toCSV(filename, active_books):
    # Clean column headers to ensure consistency
    books = clean_column_headers(active_books)

    try:
        # Open the CSV file for writing
        with open(filename, 'w', newline='', encoding='utf-8', errors='replace') as csvfile:
            # Get the fieldnames (column headers) from the first book in the list
            fieldnames = [col for col in books[0].keys()]

            # Create a CSV DictWriter
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header row to the CSV file
            writer.writeheader()

            # Write each book as a row in the CSV file
            for book in books:
                writer.writerow(book)
    except:
        # Handle any errors that occur during file writing
        print("Error saving file. Please try again")

    # Print a message indicating that the books have been saved to the CSV file
    print(f"Books have been saved to {filename}")


# Main program loop
def main():
    while True:
        print()
        print("\t===============================================")
        print("\t                    MENU                       ")
        print("\t===============================================")
        print("\t 1.  Load the books collection form CSV")
        print("\t 2.  Save the book collection to a CSV file")
        print("\t 3.  List all the books in the books collection")
        print("\t 4.  Show Info of a Book")
        print("\t 5.  Insert a book to the books collection")
        print("\t 6.  Delete the books from the books collection")
        print("\t 7.  Sort the books in the books collection")
        print("\t 8.  Search the books from the books collection")
        print("\t 9.  Staticstics of the book collection")
        print("\t 10. Update the data of specific book")

        print("\t 0. Exit the program")
        print("\t CLR : Clear the Book Directory")
        print()
        choice = input("Enter your choice: ").upper()

        if choice == "0":
            print("Exiting Program......\n Goodbye!")
            break
        if choice == "1":
            filename = input("Enter the filename: ")
            load_books(filename)
        elif choice == "2":
            filename = input(
                "Enter the filename to save with extension(eg., test.csv): ")
            save_books_toCSV(filename, active_books)
        elif choice == "3":
            list_books(active_books)
        elif choice == "4":

            show_book_info()
        elif choice == "5":
            print("Enter the book details")
            insert_book()
        elif choice == "6":
            delete_book()
        elif choice == "7":

            sort_books()
        elif choice == "8":
            search_books()
        elif choice == "9":
            calculate_statistics(active_books)
        elif choice == "10":
            update_books()
        elif choice == "CLR":

            active_books.clear()
            print("Book Directory has been cleared!")
        else:
            print("Invalid choice. Please try again.")

        # menu_navigation()


if __name__ == "__main__":
    main()
