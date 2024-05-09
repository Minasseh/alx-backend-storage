--a SQL script that creates a table users
CREATE TABLE IF NOT EXISTS users (
	id NOT NULL AUTO INCREMENT PRIMARY KEY,
	email VARCHAR(255) NOT NULL UNIQUE,
	name VARCHAR(255)
);
