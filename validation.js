
document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll("[data-form]");

    forms.forEach(function (form) {
        // We display our own validation messages.
        form.noValidate = true;

        form.addEventListener("submit", function (event) {
            const type = form.dataset.form;
            const errors = [];

            const name = form.querySelector('[name="name"]');
            const email = form.querySelector('[name="email"]');
            const password = form.querySelector('[name="password"]');
            const confirmPassword =
                form.querySelector('[name="confirm_password"]');
            const title = form.querySelector('[name="title"]');

            // Register validation
            if (type === "register") {
                if (!name.value.trim()) {
                    errors.push("Name is required");
                } else if (name.value.trim().length > 100) {
                    errors.push("Name is too long");
                }

                if (!email.value.trim()) {
                    errors.push("Email is required");
                } else if (!email.validity.valid) {
                    errors.push("Please enter a valid email address");
                }

                if (!password.value) {
                    errors.push("Password is required");
                }

                if (!confirmPassword.value) {
                    errors.push("Confirm password is required");
                }

                if (
                    password.value &&
                    confirmPassword.value &&
                    password.value !== confirmPassword.value
                ) {
                    errors.push("Passwords do not match");
                }
            }

            // Login validation
            if (type === "login") {
                if (!email.value.trim()) {
                    errors.push("Email is required");
                } else if (!email.validity.valid) {
                    errors.push("Please enter a valid email address");
                }

                if (!password.value) {
                    errors.push("Password is required");
                }
            }

            // Add and edit to-do validation
            if (type === "todo") {
                if (!title.value.trim()) {
                    errors.push("Title is required");
                } else if (title.value.trim().length > 200) {
                    errors.push(
                        "Title is too long (200 characters at most)"
                    );
                }
            }

            // Remove previous client-side errors
            const oldErrors = form.querySelector(".client-errors");

            if (oldErrors) {
                oldErrors.remove();
            }

            // Stop submission if there are errors
            if (errors.length > 0) {
                event.preventDefault();

                const errorBox = document.createElement("div");
                errorBox.className = "client-errors";

                errors.forEach(function (message) {
                    const paragraph = document.createElement("p");
                    paragraph.className = "error";
                    paragraph.textContent = message;
                    errorBox.appendChild(paragraph);
                });

                form.prepend(errorBox);
            }
        });
    });
});
