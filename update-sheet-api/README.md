# Checkout IPN

\*\*In this project, I built a webhook to handle order information when a user makes a successful payment, along with some simple CRUD APIs.

I implemented the Unit of Work pattern to ensure that the Atomicity in ACID is not violated. The idea is to move the commit and rollback logic, along with the try-catch block, to the highest layer, which is the router. This way, the service layer doesn’t have to worry about commit or rollback logic, and services can call each other with ease.\*\*

Remember to create python virtual env before installing libraries

install libraries/dependencies:

- pip install -r requirements/base.txt
- pip install -r requirements/dev.txt

command to run this project: uvicorn src.main:app --reload
