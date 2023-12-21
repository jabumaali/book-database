# app.py

from models import (Base, session, Book, engine)

# Main menu
# View, add, search, analysis, exit

# Functions:
# Add book
# Edit book
# Delete book
# Search book
# Data cleaning

if __name__ == '__main__':
    Base.metadata.create_all(engine)