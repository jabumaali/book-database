from models import (Base, session, Book, engine)
import datetime
import csv
import time

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

def menu():
    first = True
    while True:
        print("""
              \n PROGRAMMING BOOKS
              \r  1) Add Book
              \r  2) View All Books
              \r  3) Search For Book
              \r  4) Book Analysis
              \r  5) Exit Program""")
        if first == True:
            choice = input(' What would like to do? ')
            first = False
        else:
            choice = input(' What would like to do next? ')
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            print('\n Please choose one of the options above.')


def clean_date(date_str):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    split_date = date_str.split(' ')
    try:
        month = months.index(split_date[0]) + 1
        day = int(split_date[1].split(',')[0])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input('''\n ** Date Error **
                 \r Please enter date in correct format.
                 \r Press enter to continue.''')
        print('')
        return
    else:
        return return_date

def clean_price(price_str):
    try:
        final_price = round(float(price_str)*100)
    except ValueError:
        input('''\n ** Price Error **
                 \r Please enter price in correct format.
                 \r Press enter to continue.''')
        print('')
    else:
        return final_price

def view_books():
    print('\n')
    print ("{:<5} {:<40} {:<25} {:<15} {:<6}".format(
        'Id','Title','Author','Published','Price'))
    for book in session.query(Book):
        print ("{:<5} {:<40} {:<25} {:<15} {:<6}".format(
            book.id, book.title,book.author, book.published_date.strftime(
                "%b %d, %Y"), "$"+str(round(float(book.price/100),2))))


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            title = input('Title: ')
            author = input('Author: ')
            date_error = True
            while date_error:
                date = input('Published (ex. October 27, 2023): ')
                date = clean_date(date)
                if type(date) == datetime.date:
                    date_error = False
            price_error = True
            while price_error:
                price = input('Price (Ex. 14.99): ')
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            new_book = Book(title=title, author=author, published_date=date, price=price)
            session.add(new_book)
            session.commit()
            print('Book added!')
            time.sleep(1.0)
        
        elif choice == '2':
            view_books()
        
        elif choice == '3':
            id_options = []
            for book in session.query(Book):
                id_options.append(book.id)
            print(f'Your options are {id_options}.')
            try:
                id_choice = int(input('Please select your book ID: '))
            except (ValueError, ):
                print('Error: Please enter a valid book ID.')
            else:
                if id_choice in id_options:
                    for book in session.query(Book):
                        if id_choice == book.id:
                            print ("{:<5} {:<40} {:<25} {:<15} {:<6}".format(
                                'Id','Title','Author','Published','Price'))
                            print ("{:<5} {:<40} {:<25} {:<15} {:<6}".format(
                                book.id, book.title,book.author, book.published_date.strftime(
                                    "%b %d, %Y"), "$"+str(round(float(book.price/100),2))))
                else:
                    print('Error: Please enter a valid book ID.')

        elif choice == '4':
            #Analysis
            pass
        else:
            print(" Goodbye! ^_^")
            app_running = False

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()

    # for book in session.query(Book):
    #     print(book)