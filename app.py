from models import (Base, session, Book, engine)
import datetime
import csv

def menu():
    while True:
        print("""
              \n PROGRAMMING BOOKS
              \r  1) Add Book
              \r  2) View All Books
              \r  3) Search For Book
              \r  4) Book Analysis
              \r  5) Exit Program""")
        choice = input(' What would like to do? ')
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            print('\n Please choose one of the options above.')


# Functions:
# Add book
# Edit book
# Delete book
# Search book
# Data cleaning
def clean_date(date_str):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    split_date = date_str.split(' ')
    month = months.index(split_date[0]) + 1
    day = int(split_date[1].split(',')[0])
    year = int(split_date[2])
    return datetime.date(year, month, day)

def clean_price(price_str):
    return int(float(price_str)*100)


def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            book_in_db = session.query(Book).filter(Book.title==row[0]).one_or_none()
            if book_in_db == None:
                print(row)
                title = row[0]
                author = row[1]
                date = clean_date(row[2])
                price = clean_price(row[3])
                new_book = Book(title=title, author=author, published_date=date, price=price)
                session.add(new_book)
        session.commit()



def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            #Add book
            pass
        elif choice == '2':
            #View book
            pass
        elif choice == '3':
            #Search
            pass
        elif choice == '4':
            #Analysis
            pass
        else:
            print(" Goodbye! ^_^")
            app_running = False

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # app()
    add_csv()
    # clean_date()
    for book in session.query(Book):
        print(book)