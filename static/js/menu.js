// menu.js
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.icon_nav');
    const sidebar = document.getElementById('sidebar');
    const closeMenu = document.querySelector('.close-menu');

    menuToggle.addEventListener('click', function() {
        sidebar.classList.toggle('visible');
    });
    closeMenu.addEventListener('click', function() {
        sidebar.classList.remove('visible');
    });
});
