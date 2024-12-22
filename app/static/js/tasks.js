document.addEventListener('DOMContentLoaded', () => {
    const todoItems = document.querySelectorAll('.todo-item');
    const columns = document.querySelectorAll('.todo-column');
    const addTaskForms = document.querySelectorAll('.add-task-form');

    let draggedItem = null;

    todoItems.forEach(item => {
        setupDragAndDrop(item);
    });

    function setupDragAndDrop(item) {
        item.addEventListener('dragstart', (e) => {
            draggedItem = item;
            setTimeout(() => {
                item.classList.add('dragging');
            }, 0);
        });

        item.addEventListener('dragend', () => {
            draggedItem.classList.remove('dragging');
            draggedItem = null;
        });
    }

    columns.forEach(column => {
        column.addEventListener('dragover', (e) => {
            e.preventDefault();
            column.classList.add('droppable-hover');
        });

        column.addEventListener('dragleave', () => {
            column.classList.remove('droppable-hover');
        });

        column.addEventListener('drop', (e) => {
            e.preventDefault();
            column.classList.remove('droppable-hover');
            const itemsContainer = column.querySelector('.items-container');
            if (draggedItem) {
                itemsContainer.appendChild(draggedItem);
            }
        });
    });

    // Обработчик отправки формы
    addTaskForms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();  // Отменяем стандартную отправку формы

            const statusId = form.querySelector('input[name="status_id"]').value;
            const userId = form.querySelector('input[name="user_id"]').value;
            const title = form.querySelector('input[name="title"]').value;
            const description = form.querySelector('textarea[name="description"]').value;
            const deadline = form.querySelector('input[name="deadline"]').value;

            const taskData = {
                status_id: statusId,
                user_id: userId,
                title: title,
                description: description,
                deadline: deadline
            };

            try {
                const response = await fetch('/assigned_tasks/create', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(taskData),
                });

                if (response.ok) {
                    const newTask = await response.json();
                    console.log('Task created successfully:', newTask);
                    // Возможно, обновить UI, добавив новую задачу в соответствующий статус
                } else {
                    const errorData = await response.json();
                    console.error('Error creating task:', errorData);
                }
            } catch (error) {
                console.error('Network error:', error);
            }
        });
    });
});
