document.addEventListener("DOMContentLoaded", function() {
    const navbar = document.getElementById("navbar");
    
    
    if (navbar.classList.contains("navbar-transparent")) {
        window.addEventListener("scroll", function() {
            
            if (window.scrollY > 700) {
                navbar.classList.remove("navbar-transparent");
                navbar.classList.add("bg-primary");
            } else {
                navbar.classList.remove("bg-primary");
                navbar.classList.add("navbar-transparent");
            }
        });
    }
});
