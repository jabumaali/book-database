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
    while True:
        print("""
              \nPROGRAMMING BOOKS
              \r1) Add Book
              \r2) View All Books
              \r3) Search For Book
              \r4) Book Analysis
              \r5) Exit Program""")
        choice = input('What would like to do? ')
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            print('\n Please choose one of the options above.')

def submenu():
    while True:
        print("""
              \n1) Edit
              \r2) Delete
              \r3) Return to Main Menu
              """)
        choice = input('What would like to do? ')
        if choice in ['1', '2', '3']:
            return choice
        else:
            print('\n Please choose one of the options above.')

def edit_check(column_name, current_value):
    print(f'\n**** EDIT {column_name} ****')
    if column_name == 'Price':
        print(f'\rCurrent Value: {current_value/100}')
    elif column_name == 'Date':
        print(f'\rCurrent Value: {current_value.strftime("%b %d, %Y")}')
    else:
        print(f'\rCurrent Value: {current_value}')
    
    if column_name == 'Date' or column_name == 'Price':
        while True:
            changes = input('What would you like to change the value to? ')
            if column_name == 'Date':
                changes = clean_date(changes)
                if type(changes) == datetime.date:
                    return changes
            elif column_name == 'Price':
                changes = clean_price(changes)
                if type(changes) == int:
                    return changes
    else:
        return input('What would you like to change the value to? ')
    return

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

def view_books(like_this):
    print ("{:<5} {:<40} {:<25} {:<15} {:<6}".format(
        'Id','Title','Author','Published','Price'))
    for book in session.query(Book).filter(Book.title.like(like_this)):
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
            view_books("%")
        
        elif choice == '3':
            print("""\nHow would you like to search?
              \n1) By ID
              \r2) By keyword
              \r3) Return to Main Menu\n
              """)
            choice = input('What would like to do? ')
            if choice == "1":
                id_options = []
                for book in session.query(Book):
                    id_options.append(book.id)
                print(f'Your options are {id_options}.')
                try:
                    id_choice = int(input('Please select your book ID: '))
                except ValueError:
                    print('Error: Please enter a valid book ID.')
                else:
                    if id_choice in id_options:
                        the_book = session.query(Book).filter(Book.id==id_choice).first()
                        print ("{:<5} {:<40} {:<25} {:<15} {:<6}".format(
                                'Id','Title','Author','Published','Price'))
                        print ("{:<5} {:<40} {:<25} {:<15} {:<6}".format(
                                the_book.id, the_book.title, the_book.author, the_book.published_date.strftime(
                                "%b %d, %Y"), "$"+str(round(float(the_book.price/100),2))))
                    else:
                        print('Error: Please enter a valid book ID.')
                sub_choice = submenu()
                if sub_choice == '1':
                    the_book.title = edit_check('Title', the_book.title)
                    the_book.author = edit_check('Author', the_book.author)
                    the_book.published_date = edit_check('Date', the_book.published_date)
                    the_book.price = edit_check('Price', the_book.price)
                    session.commit()
                    print('Book updated!')
                    time.sleep(1.5)
                elif sub_choice == '2':
                    session.delete(the_book)
                    session.commit()
                    print('Book deleted!')
                    time.sleep(1.5)
            elif choice == "2":
                choice = input("Please enter a keyword: ")
                view_books("%"+choice+"%")
            else:
                pass


        elif choice == '4':
            oldest_book = session.query(Book).order_by(Book.published_date).first()
            newest_book = session.query(Book).order_by(Book.published_date.desc()).first()
            print("\nOldest book:", oldest_book.title + ", published on", oldest_book.published_date)
            view_books(oldest_book.title)
            print("Newest book:", newest_book.title + ", published on", newest_book.published_date)
            view_books(newest_book.title)
            print("\nPython books: ")
            view_books("%Python%")


        else:
            print("\nGoodbye! ^_^")
            app_running = False

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()
    