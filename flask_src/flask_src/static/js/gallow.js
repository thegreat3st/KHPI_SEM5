document.addEventListener("DOMContentLoaded", function () {
    const themeButtons = document.querySelectorAll(".theme-button");
    const wordInputContainer = document.getElementById("word-input-container");

    // Function to create and display tooltips
    const createTooltip = (button, description) => {
        let tooltip = button.querySelector(".theme-tooltip");
        if (!tooltip) {
            tooltip = document.createElement("div");
            tooltip.className = "theme-tooltip";
            tooltip.innerText = description;

            // Append tooltip to button
            button.appendChild(tooltip);

            // Positioning the tooltip
            tooltip.style.position = "absolute";
            tooltip.style.top = `${button.offsetHeight + 5}px`;
            tooltip.style.left = "50%";
            tooltip.style.transform = "translateX(-50%)";
            tooltip.style.backgroundColor = "#333";
            tooltip.style.color = "#fff";
            tooltip.style.padding = "5px 10px";
            tooltip.style.borderRadius = "4px";
            tooltip.style.fontSize = "14px";
            tooltip.style.boxShadow = "0 2px 5px rgba(0, 0, 0, 0.3)";
            tooltip.style.zIndex = "10";
        }
    };

    // Add event listeners to theme buttons
    themeButtons.forEach((button) => {
        const description = button.getAttribute("data-description");

        // Show tooltip on hover
        button.addEventListener("mouseover", function () {
            createTooltip(this, description);
        });

        // Remove tooltip on mouseout
        button.addEventListener("mouseout", function () {
            const tooltip = this.querySelector(".theme-tooltip");
            if (tooltip) {
                tooltip.remove();
            }
        });

        // Handle theme selection
        button.addEventListener("click", async function () {
            const theme = this.getAttribute("data-theme");
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute("content");
            // const csrfToken = "{{ csrf_token() }}";  // CSRF token
            // const csrfToken = document.querySelector('input[name="csrf_token"]').value;
            // const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute("content");
            try {
                const response = await fetch("{{ url_for('public.lab4_sample.select_theme') }}", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrfToken,
                    },
                    body: JSON.stringify({ theme }),
                });

                if (response.ok) {
                    // Hide theme buttons and show word input container
                    document.getElementById("theme-buttons").style.display = "none";
                    wordInputContainer.classList.remove("hidden");
                    wordInputContainer.classList.add("slide-up");
                } else {
                    console.error("Failed to select theme.");
                }
            } catch (error) {
                console.error("Error during theme selection:", error);
            }
        });
    });
});
