// Tema claro/oscuro. Igual que en el portfolio original, pero ahora se guarda
// la elección en localStorage para que el blog (otra página) la respete.
(function () {
    const body = document.body;
    const toggle = document.getElementById("theme-toggle");
    const icon = toggle.querySelector("i");

    function apply(light) {
        body.classList.toggle("light-mode", light);
        icon.classList.toggle("fa-sun", light);
        icon.classList.toggle("fa-moon", !light);
    }

    let saved = null;
    try { saved = localStorage.getItem("theme"); } catch (e) { /* modo privado */ }
    apply(saved === "light");

    toggle.addEventListener("click", function () {
        const light = !body.classList.contains("light-mode");
        apply(light);
        try { localStorage.setItem("theme", light ? "light" : "dark"); } catch (e) { }
    });
})();
