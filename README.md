[![Watch the video](https://img.youtube.com)](https://youtu.be/5mN5PgrlTis)
# Simple RDBMS
This project implements a simplified relational database management system.

## Features
- SQL-like interface
- Table creation with schema
- INT, TEXT, BOOL data types
- PRIMARY KEY and UNIQUE constraints
- Hash-based indexing
- INNER JOIN support
- Interactive REPL
- Web demo using FastAPI

## Architecture
- Custom database engine (no ORM, no real DB)
- REPL and web app both consume the same engine
- FastAPI used only as a presentation layer

## Limitations
- No transactions
- No concurrency
- No disk persistence
- Limited SQL grammar
- UPDATE/DELETE intentionally minimal

## AI Usage
AI tools (ChatGPT) were used for design discussion and code review.
All architecture decisions and implementation understanding are my own.

## How to Run

### Run REPL
```bash
python -m db.repl
Type SQL commands interactively. Example:

sql
Copy code
CREATE TABLE users (id INT PRIMARY, email TEXT UNIQUE, active BOOL);
INSERT INTO users (1, "marshall@example.com", true);
SELECT * FROM users;
UPDATE users SET active=false WHERE id=1;
DELETE FROM users WHERE id=1;
Run Web App
bash
Copy code
uvicorn web.app:app --reload
Web API Test Commands (cURL)
Create a user

bash
Copy code
curl -X POST "http://127.0.0.1:8000/users?id=1&name=Alice&active=true"
Get all users

bash
Copy code
curl -X GET "http://127.0.0.1:8000/users"
Update a user

bash
Copy code
curl -X PUT "http://127.0.0.1:8000/users?id=1&name=Alice2&active=false"
Delete a user

bash
Copy code
curl -X DELETE "http://127.0.0.1:8000/users?id=1"
Test SQL Commands (REPL)
sql
Copy code
-- Create users table
CREATE TABLE users (id INT PRIMARY, email TEXT UNIQUE, active BOOL);

-- Create orders table
CREATE TABLE orders (id INT PRIMARY, user_id INT, item TEXT, price INT);

-- Insert sample users
INSERT INTO users (1, "marshall@example.com", true);
INSERT INTO users (2, "alice@example.com", true);
INSERT INTO users (3, "bob@example.com", false);

-- Insert sample orders
INSERT INTO orders (1, 1, "Laptop", 1200);
INSERT INTO orders (2, 2, "Phone", 800);
INSERT INTO orders (3, 1, "Keyboard", 100);

-- Read all users
SELECT * FROM users;

-- Read all orders
SELECT * FROM orders;

-- Update a user
UPDATE users SET active=false WHERE id=2;

-- Delete a user
DELETE FROM users WHERE id=3;

-- INNER JOIN example: get user emails with their orders
SELECT users.email, orders.item, orders.price FROM users INNER JOIN orders ON users.id = orders.user_id
