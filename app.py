import os
from functools import wraps

import bcrypt
import pymysql
from dotenv import load_dotenv
from flask import Flask, request, redirect, render_template, session, url_for
from werkzeug.utils import secure_filename
import uuid
from pymysql.err import IntegrityError

from db import get_connection, get_library_connection

load_dotenv()

app = Flask(__name__)
secret_key = os.getenv("SECRET_KEY")

if not secret_key:
    raise RuntimeError("SECRET_KEY is missing from .env")

app.secret_key = secret_key


UPLOAD_FOLDER = os.path.join(app.static_folder, "uploads")
os.makedirs(os.path.join(UPLOAD_FOLDER, "books"), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, "authors"), exist_ok=True)



def save_image(file, folder):
    if not file or file.filename == "":
        return None

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in [".jpg", ".jpeg", ".png", ".webp"]:
        return None

    new_filename = str(uuid.uuid4()) + extension

    file_path = os.path.join(
        UPLOAD_FOLDER,
        folder,
        new_filename
    )

    file.save(file_path)

    return "uploads/" + folder + "/" + new_filename



def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")

        return func(*args, **kwargs)

    return wrapper


@app.route("/")
def home():
    if "user_id" in session:
        return redirect("/todos")

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register():
    errors = []

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not name:
            errors.append("Name is required")

        if not email:
            errors.append("Email is required")

        if not password:
            errors.append("Password is required")

        if not confirm_password:
            errors.append("Confirm password is required")

        if password and confirm_password and password != confirm_password:
            errors.append("Passwords do not match")

        if len(name) > 100:
            errors.append("Name is too long")

        if not errors:
            password_hash = bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            connection = get_connection()
            cursor = connection.cursor()

            try:
                cursor.execute(
                    "INSERT INTO users (email, name, password_hash) "
                    "VALUES (%s, %s, %s)",
                    (email, name, password_hash)
                )

                connection.commit()

                cursor.execute(
                    "SELECT user_id, name FROM users WHERE email = %s",
                    (email,)
                )

                user = cursor.fetchone()

                session.clear()
                session["user_id"] = user[0]
                session["name"] = user[1]

                return redirect("/todos")

            except IntegrityError:
                connection.rollback()
                errors.append("Email Already Exists")

            finally:
                cursor.close()
                connection.close()

    return render_template("register.html", errors=errors)


@app.route("/login", methods=["GET", "POST"])
def login():
    errors = []

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email:
            errors.append("Email is required")

        if not password:
            errors.append("Password is required")

        if not errors:
            connection = get_connection()
            cursor = connection.cursor()

            try:
                cursor.execute(
                    "SELECT user_id, name, password_hash "
                    "FROM users WHERE email = %s",
                    (email,)
                )

                user = cursor.fetchone()

                if user:
                    try:
                        valid_password = bcrypt.checkpw(
                            password.encode("utf-8"),
                            user[2].encode("utf-8")
                        )
                    except ValueError:
                        valid_password = False
                else:
                    valid_password = False

                if user and valid_password:
                    session.clear()
                    session["user_id"] = user[0]
                    session["name"] = user[1]

                    return redirect("/todos")

                errors.append("Invalid email or password")

            finally:
                cursor.close()
                connection.close()

    return render_template("login.html", errors=errors)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/login")


@app.route("/todos")
@login_required
def todos():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT todo_id, title, is_done, created_at "
            "FROM todos WHERE user_id = %s ORDER BY todo_id DESC",
            (session["user_id"],)
        )

        tasks = cursor.fetchall()

    finally:
        cursor.close()
        connection.close()

    return render_template(
        "todos.html",
        tasks=tasks,
        name=session["name"],
        error=request.args.get("error", "")
    )


@app.route("/add_todo", methods=["GET", "POST"])
@login_required
def add_todo():
    errors = []

    if request.method == "POST":
        title = request.form.get("title", "").strip()

        if not title:
            errors.append("Title is required")
        elif len(title) > 200:
            errors.append("Title is too long (200 characters at most)")

        if not errors:
            connection = get_connection()
            cursor = connection.cursor()

            try:
                cursor.execute(
                    "INSERT INTO todos (user_id, title) VALUES (%s, %s)",
                    (session["user_id"], title)
                )

                connection.commit()

                return redirect("/todos")

            finally:
                cursor.close()
                connection.close()

    return render_template("add_todo.html", errors=errors)


@app.route("/edit_todo/<int:todo_id>", methods=["POST"])
@login_required
def edit_todo(todo_id):
    title = request.form.get("title", "").strip()

    if not title:
        return redirect("/todos?error=Title%20is%20required")

    if len(title) > 200:
        return redirect(
            "/todos?error=Title%20is%20too%20long%20(200%20characters%20at%20most)"
        )

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "UPDATE todos SET title = %s "
            "WHERE todo_id = %s AND user_id = %s",
            (title, todo_id, session["user_id"])
        )

        connection.commit()

    finally:
        cursor.close()
        connection.close()

    return redirect("/todos")


@app.route("/toggle_todo/<int:todo_id>", methods=["POST"])
@login_required
def toggle_todo(todo_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT is_done FROM todos "
            "WHERE todo_id = %s AND user_id = %s",
            (todo_id, session["user_id"])
        )

        task = cursor.fetchone()

        if task:
            new_status = 1 - task[0]

            cursor.execute(
                "UPDATE todos SET is_done = %s "
                "WHERE todo_id = %s AND user_id = %s",
                (new_status, todo_id, session["user_id"])
            )

            connection.commit()

    finally:
        cursor.close()
        connection.close()

    return redirect("/todos")


@app.route("/delete_todo/<int:todo_id>", methods=["POST"])
@login_required
def delete_todo(todo_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM todos WHERE todo_id = %s AND user_id = %s",
            (todo_id, session["user_id"])
        )

        connection.commit()

    finally:
        cursor.close()
        connection.close()

    return redirect("/todos")


@app.route("/library")
@login_required
def library():
    connection = get_library_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT book_id, title, price, author_id, image FROM book"
        )
        books = cursor.fetchall()

        cursor.execute(
            "SELECT author_id, name, country, image FROM author"
        )
        authors = cursor.fetchall()

    finally:
        cursor.close()
        connection.close()

    return render_template(
        "library.html",
        books=books,
        authors=authors,
        name=session["name"]
    )


@app.route("/add_author", methods=["GET", "POST"])
@login_required
def add_author():
    errors = []

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        country = request.form.get("country", "").strip()
        author_image = request.files.get("author_image")
        image_path = None

        if not name:
            errors.append("Author name is required")

        if len(name) > 100:
            errors.append("Author name is too long")

        if author_image and author_image.filename:
            image_path = save_image(author_image, "authors")

            if image_path is None:
                errors.append("Choose a valid image: JPG, PNG or WEBP")

        if not errors:
            connection = get_library_connection()
            cursor = connection.cursor()

            try:
                cursor.execute(
                    "INSERT INTO author (name, country, image) "
                    "VALUES (%s, %s, %s)",
                    (name, country, image_path)
                )

                connection.commit()
                return redirect("/library")

            finally:
                cursor.close()
                connection.close()

    return render_template("add_author.html", errors=errors)


@app.route("/add_book", methods=["GET", "POST"])
@login_required
def add_book():
    errors = []

    connection = get_library_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT author_id, name FROM author")
        authors = cursor.fetchall()

        if request.method == "POST":
            title = request.form.get("title", "").strip()
            price = request.form.get("price", "").strip()
            author_id = request.form.get("author_id", "").strip()
            book_image = request.files.get("book_image")
            image_path = None

            if not title:
                errors.append("Book title is required")
            elif len(title) > 200:
                errors.append("Book title is too long")

            try:
                price = float(price)

                if price < 0:
                    errors.append("Price cannot be negative")

            except ValueError:
                errors.append("Enter a valid price")

            try:
                author_id = int(author_id)

                if author_id not in [author[0] for author in authors]:
                    errors.append("Select a valid author")

            except ValueError:
                errors.append("Select an author")

            if book_image and book_image.filename:
                image_path = save_image(book_image, "books")

                if image_path is None:
                    errors.append("Choose a valid image: JPG, PNG or WEBP")

            if not errors:
                cursor.execute(
                    "INSERT INTO book (title, price, author_id, image) "
                    "VALUES (%s, %s, %s, %s)",
                    (title, price, author_id, image_path)
                )

                connection.commit()
                return redirect("/library")

    finally:
        cursor.close()
        connection.close()

    return render_template(
        "add_book.html",
        errors=errors,
        authors=authors
    )


@app.route("/edit_book/<int:book_id>", methods=["GET", "POST"])
@login_required
def edit_book(book_id):
    errors = []
    connection = get_library_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT book_id, title, price, author_id, image FROM book WHERE book_id = %s",
            (book_id,)
        )
        book = cursor.fetchone()

        if not book:
            return redirect("/library?error=Book%20not%20found")

        cursor.execute("SELECT author_id, name FROM author")
        authors = cursor.fetchall()

        if request.method == "POST":
            title = request.form.get("title", "").strip()
            price_text = request.form.get("price", "").strip()
            author_id_text = request.form.get("author_id", "").strip()
            book_image = request.files.get("book_image")
            image_path = book[4]

            if not title:
                errors.append("Book title is required")
            elif len(title) > 200:
                errors.append("Book title is too long")

            try:
                price = float(price_text)
                if price < 0:
                    errors.append("Price cannot be negative")
            except ValueError:
                price = None
                errors.append("Enter a valid price")

            try:
                author_id = int(author_id_text)
                if author_id not in [author[0] for author in authors]:
                    errors.append("Select a valid author")
            except ValueError:
                author_id = None
                errors.append("Select an author")

            if book_image and book_image.filename:
                new_image_path = save_image(book_image, "books")

                if new_image_path is None:
                    errors.append("Choose a valid image: JPG, PNG or WEBP")
                else:
                    image_path = new_image_path

            if not errors:
                cursor.execute(
                    "UPDATE book SET title = %s, price = %s, author_id = %s, image = %s "
                    "WHERE book_id = %s",
                    (title, price, author_id, image_path, book_id)
                )

                connection.commit()
                return redirect("/library")

        return render_template(
            "edit_book.html",
            book=book,
            authors=authors,
            errors=errors
        )

    finally:
        cursor.close()
        connection.close()



@app.route("/edit_author/<int:author_id>", methods=["GET", "POST"])
@login_required
def edit_author(author_id):
    errors = []
    connection = get_library_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT author_id, name, country, image FROM author WHERE author_id = %s",
            (author_id,)
        )
        author = cursor.fetchone()

        if not author:
            return redirect("/library?error=Author%20not%20found")

        if request.method == "POST":
            name = request.form.get("name", "").strip()
            country = request.form.get("country", "").strip()
            author_image = request.files.get("author_image")
            image_path = author[3]

            if not name:
                errors.append("Author name is required")
            elif len(name) > 100:
                errors.append("Author name is too long")

            if author_image and author_image.filename:
                new_image_path = save_image(author_image, "authors")

                if new_image_path is None:
                    errors.append("Choose a valid image: JPG, PNG or WEBP")
                else:
                    image_path = new_image_path

            if not errors:
                cursor.execute(
                    "UPDATE author SET name = %s, country = %s, image = %s "
                    "WHERE author_id = %s",
                    (name, country, image_path, author_id)
                )

                connection.commit()
                return redirect("/library")

        return render_template(
            "edit_author.html",
            author=author,
            errors=errors
        )

    finally:
        cursor.close()
        connection.close()



@app.route("/delete_book/<int:book_id>", methods=["POST"])
@login_required
def delete_book(book_id):
    connection = get_library_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM book WHERE book_id = %s",
            (book_id,)
        )
        connection.commit()

    finally:
        cursor.close()
        connection.close()

    return redirect("/library")



@app.route("/delete_author/<int:author_id>", methods=["POST"])
@login_required
def delete_author(author_id):
    connection = get_library_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM author WHERE author_id = %s",
            (author_id,)
        )
        connection.commit()

    except IntegrityError:
        connection.rollback()
        return redirect(
            "/library?error=Author%20could%20not%20be%20deleted.%20Check%20ON%20DELETE%20CASCADE"
        )

    finally:
        cursor.close()
        connection.close()

    return redirect("/library")

if __name__ == "__main__":
    app.run(debug=True)