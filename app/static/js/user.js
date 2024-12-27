document.addEventListener("DOMContentLoaded", () => {
    const userTable = document.getElementById("user-table").querySelector("tbody");

    async function fetchUsers() {
        const response = await fetch('/auth/users/list');
        const users = await response.json();

        const responseUserTypes = await fetch('/usertype/list');
        const userTypes = await responseUserTypes.json();

        userTable.innerHTML = ""; // Очистить перед добавлением
        users.forEach(user => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${user.id}</td>
                <td>${user.name}</td>
                <td>${user.email}</td>
                <td>
                    <select data-user-id="${user.id}">
                        ${userTypes.map(type => `
                            <option value="${type.id}" ${type.id === user.usertype ? 'selected' : ''}>
                                ${type.usertype}
                            </option>
                        `).join('')}
                    </select>
                </td>
                <td>
                    <button data-user-id="${user.id}" class="save-button">Сохранить</button>
                </td>
            `;

            userTable.appendChild(row);
        });

        attachEventListeners();
    }

    function attachEventListeners() {
        document.querySelectorAll(".save-button").forEach(button => {
            button.addEventListener("click", async (event) => {
                const userId = event.target.dataset.userId;
                const selectElement = document.querySelector(`select[data-user-id="${userId}"]`);
                const newUserType = selectElement.value;

                const response = await fetch(`/auth/users/update/${userId}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({usertype: parseInt(newUserType)})
                });
            });
        });
    }
    fetchUsers();
});
