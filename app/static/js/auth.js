// Переключение вкладок между авторизацией и регистрацией
const tabs = document.querySelectorAll('.tab');
const forms = document.querySelectorAll('.form');

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        // Удаляем класс "active" со всех вкладок и форм
        tabs.forEach(t => t.classList.remove('active'));
        forms.forEach(f => f.classList.remove('active'));

        // Добавляем класс "active" к выбранной вкладке и форме
        tab.classList.add('active');
        document.querySelector(`#${tab.dataset.tab}Form`).classList.add('active');
    });
});

// Функция обработки авторизации
async function handleLogin(event) {
    event.preventDefault();

    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const response = await fetch('/auth/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email,
                password
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Успешный вход
            alert('Авторизация успешна!');
            localStorage.setItem('token', data.access_token); // Сохраняем токен
            window.location.href = '/chat'; // Переход на страницу чата
        } else {
            throw new Error(data.detail || 'Ошибка авторизации');
        }
    } catch (error) {
        console.error('Ошибка:', error.message);
        alert(error.message);
    }
}

// Функция обработки регистрации
async function handleRegister(event) {
    event.preventDefault();

    const email = document.getElementById('registerEmail').value;
    const name = document.getElementById('registerName').value;
    const password = document.getElementById('registerPassword').value;
    const passwordConfirm = document.getElementById('registerPasswordConfirm').value;

    // Проверка на совпадение паролей
    if (password !== passwordConfirm) {
        alert('Пароли не совпадают');
        return;
    }

    try {
        const response = await fetch('/auth/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email,
                name,
                password,
                password_check: passwordConfirm // Отправляем проверочный пароль
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Успешная регистрация
            alert('Регистрация успешна! Теперь вы можете войти.');
            tabs[0].click(); // Переключение на вкладку "Авторизация"
        } else {
            throw new Error(data.detail || 'Ошибка регистрации');
        }
    } catch (error) {
        console.error('Ошибка:', error.message);
        alert(error.message);
    }
}
