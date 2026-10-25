DROP DATABASE IF EXISTS Library;
CREATE DATABASE IF NOT EXISTS Library;
USE Library;

CREATE TABLE AUTHOR (
    author_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(100)
);

CREATE TABLE BOOK (
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    price DECIMAL(10,2),
    author_id INT,
    FOREIGN KEY (author_id)
        REFERENCES AUTHOR(author_id)
        ON DELETE CASCADE
);



INSERT INTO author (name, country)
VALUES
('Ahmed Khaled Tawfik', 'Egypt'),
('Naguib Mahfouz', 'Egypt'),
('William Shakespeare', 'England');

INSERT INTO book (title, price, author_id)
VALUES
('Utopia', 150.00, 1),
('The Blue Elephant', 200.00, 1),
('Palace Walk', 180.00, 2),
('Miramar', 160.00, 2),
('Hamlet', 120.00, 3),
('Macbeth', 130.00, 3);


SELECT * FROM AUTHOR;
SELECT * FROM BOOK;



ALTER TABLE author
ADD COLUMN image VARCHAR(255) NULL;

ALTER TABLE book
ADD COLUMN image VARCHAR(255) NULL;


