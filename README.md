# Overview

**OrderHub** functions as an integrated system for handling restaurant table bookings and managing orders. Tailored for restaurant servers and hosts, the application includes user-focused pages enabling order placement, closure, and the assignment of tables to servers.


# Project setup

To run the application locally:

1. Clone this repository `https://github.com/alagumuthiah/OrderHub`
2. Create a `.env` file based on the `.env.example` with proper settings required for the development environment
3. Set up the virtual environment for the application. Install dependencies pipenv install -r requirements.txt
4. Activate the virtual environment using `pipenv shell`
5. Setup PostgreSQL user, password and database and to make sure it matches the .env file
6. Use `database.py` to populate the initial data in the database. This application doesn't use SQL Alembic to  seed the data.
7. Use `flask run` to run the application

# Technologies Used

- Python
- Flask
- SQLAlchemy
- WTForms
- HTML
- Jinja Templating
- PostgreSQL

# Features of the App

## Features Completed
* Employee (Server/ Host) can login to the application
* Employee can assign a table to a server
* Server can only view the orders assigned him/ her
* Server can take order by adding menu items to the order assigned
* Server can close the order with the total cost of the order

## Features to be implemented
* List the menu items category-wise
* Menu management feature - by adding menu items, creating new menu/ menu items, updating/ deleting the items

## Link to Wiki docs

[Link to Wiki Docs] [https://github.com/alagumuthiah/OrderHub/wiki]
