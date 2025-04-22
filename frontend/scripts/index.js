// User database in localStorage
const usersDB = JSON.parse(localStorage.getItem("users")) || [];

function togglePassword(id, icon) {
    const input = document.getElementById(id);
    if (input.type === "password") {
        input.type = "text";
        icon.classList.replace("fa-eye", "fa-eye-slash");
    } else {
        input.type = "password";
        icon.classList.replace("fa-eye-slash", "fa-eye");
    }
}

function showLogin() {
    document.getElementById("login-form").style.display = "block";
    document.getElementById("register-form").style.display = "none";
    clearMessages();
}

function showRegister() {
    document.getElementById("register-form").style.display = "block";
    document.getElementById("login-form").style.display = "none";
    clearMessages();
}

function showLoginModal() {
    document.getElementById("login-modal").classList.add("active");
}

function hideLoginModal() {
    document.getElementById("login-modal").classList.remove("active");
    showLogin();
}

function clearMessages() {
    document.getElementById("login-message").style.display = "none";
    document.getElementById("register-message").style.display = "none";
}

function login() {
    const username = document.getElementById("login-username").value.trim();
    const password = document.getElementById("login-password").value;
    const message = document.getElementById("login-message");

    if (!username || !password) {
        showError(message, "Please fill in all fields");
        return;
    }

    const user = usersDB.find((u) => u.username === username && u.password === password);

    if (user) {
        showSuccess(message, "Login successful!");

        // Store logged in user
        localStorage.setItem(
            "currentUser",
            JSON.stringify({
                username: user.username,
                email: user.email,
                lastLogin: new Date().toISOString()
            })
        );

        // Redirect to dashboard
        window.location.href = "dashboard.html";
    } else {
        showError(message, "Invalid username or password");
    }
}

function register() {
    const username = document.getElementById("register-username").value.trim();
    const email = document.getElementById("register-email").value.trim();
    const password = document.getElementById("register-password").value;
    const confirmPassword = document.getElementById("register-confirm-password").value;
    const message = document.getElementById("register-message");

    if (!username || !email || !password || !confirmPassword) {
        showError(message, "Please fill in all fields");
        return;
    }

    if (password !== confirmPassword) {
        showError(message, "Passwords do not match");
        return;
    }

    if (password.length < 6) {
        showError(message, "Password must be at least 6 characters");
        return;
    }

    if (usersDB.some((u) => u.username === username)) {
        showError(message, "Username already taken");
        return;
    }

    if (usersDB.some((u) => u.email === email)) {
        showError(message, "Email already registered");
        return;
    }

    // Create new user
    const newUser = {
        username,
        email,
        password,
        createdAt: new Date().toISOString()
    };

    usersDB.push(newUser);
    localStorage.setItem("users", JSON.stringify(usersDB));

    // Show success modal instead of message
    showLoginModal();

    // Clear form
    document.getElementById("register-username").value = "";
    document.getElementById("register-email").value = "";
    document.getElementById("register-password").value = "";
    document.getElementById("register-confirm-password").value = "";
}

function showError(element, message) {
    element.textContent = message;
    element.className = "message error";
    element.style.display = "block";
}

function showSuccess(element, message) {
    element.textContent = message;
    element.className = "message success";
    element.style.display = "block";
}

// Close modal when clicking outside
window.onclick = function (event) {
    if (event.target.classList.contains("modal")) {
        document.querySelectorAll(".modal").forEach((modal) => {
            modal.classList.remove("active");
        });
    }
};
