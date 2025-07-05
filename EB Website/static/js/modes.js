document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("themeToggle");
    const body = document.body;

    toggle.addEventListener("click", () => {
        body.classList.toggle("light-mode");
        toggle.classList.toggle("active");
    });
});