# 📝 Login, To-Do List & Library Management System

A web-based application developed using **Python, Flask, MySQL, HTML, CSS, and JavaScript** as part of the Introduction to Database Systems course at Alexandria National University.

The project combines a user authentication system, a personal To-Do list, and a Library Management section for managing books and authors. It demonstrates relational database design, foreign key relationships, CRUD operations, file uploads, and Flask-MySQL integration.

**Name:** Mohamed Mahmoud  
**ID:** 2304096  
**Contribution:** Database design, Flask backend, user authentication, To-Do list functionality, library management, and image upload functionality.

## ✨ Features

### 🔐 User Authentication
- **User Registration:** Create an account using a name, email, and password.
- **User Login:** Authenticate registered users.
- **Password Security:** Store passwords as bcrypt hashes instead of plain text.
- **Session Management:** Maintain the user's login session.
- **Protected Pages:** Restrict access to protected pages and task management routes.

### ✅ To-Do List
- **Personal Tasks:** Each user can manage their own tasks.
- **Add Tasks:** Create tasks with title validation.
- **Edit Tasks:** Update existing task titles.
- **Mark as Done:** Switch tasks between completed and pending.
- **Delete Tasks:** Remove tasks when they are no longer needed.
- **Task Ownership:** Users can manage only their own tasks.

### 📚 Library Management
- **Library Dashboard:** Display books and their related information.
- **View Books:** Display book IDs, titles, prices, and author IDs.
- **Add Books:** Add new books with a title, price, and author.
- **Edit Books:** Update book information.
- **Delete Books:** Remove books from the library.
- **Manage Authors:** Add, view, edit, and delete author records.
- **Author Relationships:** Associate books with authors using a foreign key.
- **Book Cover Uploads:** Upload images for books.
- **Author Photo Uploads:** Upload images for authors.
- **Image Display:** Display uploaded images in the library interface.
- **Image Validation:** Restrict image uploads to supported file extensions: JPG, JPEG, PNG, and WEBP.

### 🎨 User Interface
- Responsive layout for different screen sizes.
- Light and dark mode for the To-Do application.
- Styled forms, navigation links, and library pages.
- Input validation and error messages.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flask | Web framework and backend routing |
| MySQL | Relational database |
| PyMySQL | Connect Python to MySQL |
| bcrypt | Password hashing |
| HTML5 | Web page structure |
| CSS3 | Styling and responsive layout |
| JavaScript | Client-side validation and interface interactions |
| Jinja2 | Render dynamic HTML templates |
| Werkzeug | Secure filename handling for uploaded images |

## 🗄️ Database Design

The project uses a MySQL database named `registration`.

The database contains four main tables for users, tasks, authors, and books.

### 1. Users Table

Stores registered user information.

| Column | Description |
|---|---|
| `user_id` | Primary key; automatically generated |
| `email` | Unique user email |
| `name` | User's name |
| `password_hash` | Bcrypt password hash |
| `registration_date` | Account creation timestamp |

### 2. To-Dos Table

Stores tasks belonging to registered users.

| Column | Description |
|---|---|
| `todo_id` | Primary key; automatically generated |
| `user_id` | Foreign key referencing `users.user_id` |
| `title` | Task title |
| `is_done` | Task completion status |
| `created_at` | Task creation timestamp |

**Relationship:** One user can have multiple tasks. The `user_id` foreign key connects each task to its owner.

### 3. Author Table

Stores information about library authors.

| Column | Description |
|---|---|
| `author_id` | Primary key; author identifier |
| `name` | Author's name |
| `country` | Author's country |
| `image` | Path to the uploaded author photo, when available |

### 4. Book Table

Stores information about library books.

| Column | Description |
|---|---|
| `book_id` | Primary key; book identifier |
| `title` | Book title |
| `price` | Book price |
| `author_id` | Foreign key referencing `author.author_id` |
| `image` | Path to the uploaded book cover, when available |

**Relationship:** One author can have multiple books. The `author_id` foreign key connects each book to its author.

*Note: The author and book columns above describe the application's library features. Use the actual SQL schema in your project if your column names or data types differ.*

## 📸 Screenshots

Add screenshots of the current application to the `screenshots/` directory and update the filenames below if needed.

### 1. User Registration

![Registration Page](screenshots/register.png)

Users can create an account by entering their information.

### 2. Login Page

![Login Page](screenshots/login.png)

Registered users can log in to access their application.

### 3. My To-Do List

![To-Do List](screenshots/todo-list.png)

Users can view, add, edit, complete, and delete their personal tasks.

### 4. Add New Task

![Add Task Page](screenshots/add-task.png)

Users can add tasks to their personal To-Do list.

### 5. Library Dashboard

![Library Dashboard](screenshots/library.png)

The library dashboard displays books, prices, author information, and uploaded images.

### 6. Add Book

![Add Book Page](screenshots/add-book.png)

Users can add a book, select an author, enter the price, and upload a book cover.

### 7. Add Author

![Add Author Page](screenshots/add-author.png)

Users can add author information and upload an author photo.

## ⚙️ Installation and Setup

### Prerequisites

Make sure you have installed:

- Python 3
- MySQL Server
- Git (optional)

### Step 1: Clone the Repository

```bash
git clone https://github.com/rewansrour123/My_Todo_list.git
cd My_Todo_list
```

Alternatively, download the repository and open its folder in VS Code.

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

If your project uses environment variables, create a `.env` file in the project root directory using `.env.example` as a template.

Example configuration:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=registration
DB_PORT=3306
SECRET_KEY=replace_with_a_random_secret_key
```

Replace the example password with your actual MySQL password and use a secure, randomly generated secret key.

**Security note:** Never upload your real `.env` file or database credentials to GitHub.

### Step 5: Create the Database

Open MySQL Workbench or DBeaver and execute the SQL script that matches your current project schema.

The database should contain the tables required for:

- User registration and authentication.
- To-Do tasks.
- Authors.
- Books.

Make sure the foreign keys are configured correctly, especially the relationship between books and authors.

**Important:** If your SQL script contains `DROP DATABASE`, back up any important data before executing it.

### Step 6: Prepare the Image Upload Folders

The application stores uploaded images inside the Flask static directory.

Expected folder structure:

```text
static/
├── style.css
└── uploads/
    ├── books/
    └── authors/
```

The application creates the `books` and `authors` upload folders automatically if the corresponding code is present in `app.py`.

Uploaded image paths are stored in the database and used to display book covers and author photos.

### Step 7: Run the Application

From the project root directory, run:

```bash
python app.py
```

Open the application in your browser:

[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

Register or log in to access the protected application pages. Open the Library section to manage books and authors.

## 🔐 Security and Validation

- Passwords are hashed using bcrypt before being stored in the database.
- Parameterized SQL queries help reduce SQL injection risks.
- Protected routes require an authenticated session where configured.
- Task update and deletion operations should verify task ownership.
- Form inputs are validated on the client and server where implemented.
- Environment variables can be used for database configuration and the Flask secret key.
- Uploaded images are assigned generated filenames to avoid filename collisions.
- Supported image extensions are checked before saving uploaded files.

**Note:** Extension validation alone does not verify that an uploaded file contains valid image data.

## 📂 Project Structure

The following structure illustrates the main project components. Update filenames to match your actual repository.

```text
My_Todo_list/
├── app.py
├── db.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   ├── register.html
│   ├── login.html
│   ├── todos.html
│   ├── add_todo.html
│   ├── library.html
│   ├── add_book.html
│   ├── edit_book.html
│   ├── add_author.html
│   └── edit_author.html
├── static/
│   ├── style.css
│   └── uploads/
│       ├── books/
│       └── authors/
└── screenshots/
    ├── register.png
    ├── login.png
    ├── todo-list.png
    ├── add-task.png
    ├── library.png
    ├── add-book.png
    └── add-author.png
```

## 🎯 Learning Objectives

This project demonstrates the practical application of:

- Relational database design and SQL table creation.
- Primary keys, foreign keys, unique constraints, and referential integrity.
- Connecting a Flask application to MySQL using PyMySQL.
- Implementing registration, login, and session management.
- Performing CRUD operations: Create, Read, Update, and Delete.
- Managing relationships between authors and books.
- Handling file uploads and displaying images in a web application.
- Validating user input and handling errors.
- Building a responsive web interface.

## 👨‍💻 Author

**Mohamed Mahmoud**  
**ID:** 2304096  
Faculty of Engineering, Alexandria National University  
Introduction to Database Systems — Lab 2 and Lab 3

---

*Developed for educational purposes as part of the Fall 2026 Database Systems Labs.*
