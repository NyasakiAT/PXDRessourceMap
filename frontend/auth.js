document.getElementById("login-btn").addEventListener("click", function () {
    console.log("AUTH");

    const auth_url = "http://127.0.0.1:8000/api/auth/";
    const usernameInput = document.getElementById("username-input");
    const passwordInput = document.getElementById("password-input");

    const credentials = {
        username: usernameInput.value,
        password: passwordInput.value
    };

    fetch(auth_url, {
        method: "POST",
        headers: {
            "Content-type": "application/json; charset=UTF-8",
        },
        body: JSON.stringify(credentials),
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
    })
    .then((json) => {
        console.log(json);

        // Assuming the token is received in the JSON response, you can create a cookie
        const authToken = json.token;
        document.cookie = `auth_token=${authToken}; path=/;`;

        // Redirect back to the index page (you can change the URL as needed)
        window.location.href = "index.html";
    })
    .catch((error) => {
        console.error("Fetch error:", error);
    });
});
