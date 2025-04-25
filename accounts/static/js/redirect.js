// Wait for the document to be fully loaded
document.addEventListener("DOMContentLoaded", function () {

    // Get all forms and buttons
    const signInForm = document.querySelector("form[action='{% url 'signIn' %}']");
    const signUpForm = document.querySelector("form[action='{% url 'signup' %}']");
    const signInButton = document.querySelector(".sign-in-button");
    const signUpButton = document.querySelector(".sign-up-button");
    
    // Handle Sign In form submission
    if (signInForm) {
    signInForm.addEventListener("submit", function(event) {
    // Validate email and password
    const email = signInForm.querySelector("input[name='email']").value;
    const password = signInForm.querySelector("input[name='password']").value;
    
    if (!email || !password) {
    event.preventDefault();
    alert("Please enter both email and password.");
    return;
    }
    
    // Change button text to indicate loading
    signInButton.disabled = true;
    signInButton.textContent = "Signing In...";
    });
    }
    
    // Handle Sign Up form submission
    if (signUpForm) {
    signUpForm.addEventListener("submit", function(event) {
    // Validate form fields (name, email, and password)
    const name = signUpForm.querySelector("input[name='name']").value;
    const email = signUpForm.querySelector("input[name='email']").value;
    const password = signUpForm.querySelector("input[name='password']").value;
    
    if (!name || !email || !password) {
    event.preventDefault();
    alert("Please fill all the fields.");
    return;
    }
    
    // Change button text to indicate loading
    signUpButton.disabled = true;
    signUpButton.textContent = "Creating Account...";
    });
    }
    
    // Toggle the visibility of the sign-up/sign-in sections
    const signUpSection = document.getElementById("signUpSection");
    const signInSection = document.getElementById("signInSection");
    
    // Switch to Sign Up section
    if (signUpButton) {
    signUpButton.addEventListener("click", function () {
    signInSection.style.display = "none";
    signUpSection.style.display = "block";
    });
    }
    
    // Switch to Sign In section
    if (signInButton) {
    signInButton.addEventListener("click", function () {
    signUpSection.style.display = "none";
    signInSection.style.display = "block";
    });
    }
    
    });