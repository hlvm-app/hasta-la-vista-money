function setActiveNavLink() {
    const navLinks = document.querySelectorAll('.nav-link'); // Получаем все элементы с классом "nav-link"
    const currentURL = window.location.href; // Получаем текущий URL страницы

    navLinks.forEach(link => {
        if (link.href === currentURL) {
            link.classList.add('active'); // Добавляем класс "active" к выбранной кнопке
        } else {
            link.classList.remove('active'); // Убираем класс "active" с остальных кнопок
        }
    });
}

window.addEventListener('DOMContentLoaded', setActiveNavLink);