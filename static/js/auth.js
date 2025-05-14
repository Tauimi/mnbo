
// Скрипт обработки авторизации
document.addEventListener('DOMContentLoaded', function() {
  // Проверяем, авторизован ли пользователь
  const isLoggedIn = document.body.classList.contains('logged-in');
  
  // Обновляем элементы интерфейса при авторизации
  if (isLoggedIn) {
    console.log('Пользователь авторизован');
    
    // Устанавливаем обработчики для элементов, доступных только авторизованным пользователям
    const userMenuItems = document.querySelectorAll('.user-menu-item');
    userMenuItems.forEach(item => {
      item.addEventListener('click', function(e) {
        // Предотвращаем возможную проблему с блокировкой интерфейса
        e.stopPropagation();
      });
    });
  }
  
  // Обработчик для формы логина
  const loginForm = document.querySelector('#login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', function(e) {
      // Дополнительная валидация перед отправкой формы
      const username = loginForm.querySelector('[name="username"]').value;
      const password = loginForm.querySelector('[name="password"]').value;
      
      if (!username || !password) {
        e.preventDefault();
        alert('Пожалуйста, заполните все поля');
      }
    });
  }
});
