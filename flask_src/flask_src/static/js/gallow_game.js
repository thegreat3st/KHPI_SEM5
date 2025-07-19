document.addEventListener("DOMContentLoaded", function () {
    const letterButtons = document.querySelectorAll(".letter-button");
    const displayWord = document.getElementById("display-word");
    const incorrectLetters = document.getElementById("incorrect-letters");

    // CSRF token is embedded in the template
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute("content");

    letterButtons.forEach((button) => {
        button.addEventListener("click", async function () {
            const letter = this.getAttribute("data-letter");

            try {
                const response = await fetch(window.location.href, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json", // Explicitly set JSON content type
                        "X-CSRFToken": csrfToken // CSRF token header
                    },
                    body: JSON.stringify({ letter }) // JSON payload
                });

                if (response.ok) {
                    const data = await response.json();
                    displayWord.textContent = data.display_word;
                    incorrectLetters.textContent = data.incorrect_letters.join(", ");

                    // Disable the button and mark it as used
                    this.disabled = true;
                    this.classList.add(
                        data.display_word.includes(letter) ? "correct" : "incorrect"
                    );
                } else {
                    console.error("Server error:", await response.text());
                }
            } catch (error) {
                console.error("Request failed:", error);
            }
        });
    });
});
