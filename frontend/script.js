const signupForm = document.getElementById("signupForm");

signupForm.addEventListener("submit", function(event) {

    event.preventDefault();

    const inputs = signupForm.querySelectorAll("input");

    const name = inputs[0].value.trim();
    const email = inputs[1].value.trim();
    const password = inputs[2].value.trim();

    if (name === "" || email === "" || password === "") {
        alert("Please fill all the fields.");
        return;
    }

    // Save user information
    localStorage.setItem("userName", name);
    localStorage.setItem("userEmail", email);

    // Success message
    alert("Account created successfully!");

    // Go to the main page 
    window.location.href = "dashboard.html";
});  