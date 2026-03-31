// Register Function
function registerUser() {
    let name = document.getElementById("name").value;
    let email = document.getElementById("email").value;

    if (name === "" || email === "") {
        alert("Please fill all fields");
        return;
    }

    alert("Registration Successful (Demo)");
    window.location.href = "login.html";
}

// Login Function
function loginUser() {
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;

    if (email === "" || password === "") {
        alert("Enter email & password");
        return;
    }

    alert("Login Successful (Demo)");
    window.location.href = "dashboard.html";
}

// Logout Function
function logoutUser() {
    alert("Logged out");
    window.location.href = "login.html";
}