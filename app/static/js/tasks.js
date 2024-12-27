document.addEventListener('DOMContentLoaded', () => {
    const todoItems = document.querySelectorAll('.todo-item');  
    const columns = document.querySelectorAll('.todo-column');  
    const addTodoInputs = document.querySelectorAll('.add-todo');  
    
    let draggedItem = null;  
    let userId = null; // Получаем user_id с бекенда  
      
    
     async function fetchUserId() {  
        try {  
            const response = await fetch('/assigned-tasks/userId');  
            if (!response.ok) {  
                throw new Error(`HTTP error! Status: ${response.status}`);  
            }  
            const data = await response.json();  
            userId = data.id;  
            return data.id  
        } catch (error) {  
            console.error('Failed to fetch user ID:', error);  
             return null;  
        }  
    }  
    
    async function loadTasks() {  
        const user_id = await fetchUserId();  
        if (!user_id) return;  
        try {  
            removeAllTodoItems();  
              
            const response = await fetch(`/assigned-tasks/data/${user_id}`);  
            if (!response.ok) {  
                throw new Error(`HTTP error! Status: ${response.status}`);  
            }  
            const tasks = await response.json();  
            tasks.forEach(task => {  
                const newTodo = document.createElement('div');  
                newTodo.className = 'todo-item';  
                newTodo.draggable = true;  
                newTodo.textContent = task.task_title;  
                newTodo.dataset.taskId = task.id; // Store assigned task ID  
                  
                const column = document.querySelector(`.todo-column[data-column="${getColumnNameFromStatusId(task.status_id)}"] .items-container`);  
                if(column){  
                    column.appendChild(newTodo);  
                    setupDragAndDrop(newTodo);  
                }  
            });  
        } catch (error) {  
            console.error('Failed to load tasks:', error);  
        }  
    }  
    
    function getColumnNameFromStatusId(statusId) {  
      switch (statusId) {  
          case 1:  
              return 'todo';  
          case 2:  
              return 'in-progress';  
          case 3:  
              return 'done';  
          default:  
              return 'todo'; // default в случае чего  
      }  
    }  
      
    function getStatusIdFromColumn(column) {  
      const columnData = column.getAttribute('data-column');  
      switch (columnData) {  
        case 'todo':  
              return 1;  
        case 'in-progress':  
              return 2;  
        case 'done':  
              return 3;  
        default:  
            return 1;  
      }  
    }  
      
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
      
    // Column drop zones  
    columns.forEach(column => {  
      column.addEventListener('dragover', (e) => {  
        e.preventDefault();  
        column.classList.add('droppable-hover');  
      });  
        
      column.addEventListener('dragleave', () => {  
        column.classList.remove('droppable-hover');  
      });  
        
        column.addEventListener('drop', async (e) => {  
          e.preventDefault();  
          column.classList.remove('droppable-hover');  
          const itemsContainer = column.querySelector('.items-container');  
          if (draggedItem) {  
              const taskId = draggedItem.dataset.taskId;  
              const newStatusId = getStatusIdFromColumn(column);  
              try {  
                 await updateTaskStatus(taskId, newStatusId);  
                 itemsContainer.appendChild(draggedItem);  
              } catch (error) {
                  console.error('Failed to update task status', error);
              }
          }
      });
    });

    async function updateTaskStatus(taskId, statusId) {
        try {
            const response = await fetch(`/assigned-tasks/updateAssignedTask/${taskId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type':
  'application/json'
                },
                body: JSON.stringify({ status_id: statusId })
            });
            if (!response.ok) {
                throw new Error(`Failed to update task status. Status: ${response.status}`);
            }
            loadTasks();
        } catch (error) {
            console.error('Error updating task status:', error);
            throw error; // rethrow
        }
    }

    // Add new todo items
    addTodoInputs.forEach(input => {
      input.addEventListener('keypress', async (e) => {
        if (e.key === 'Enter' && input.value.trim() !== '') {
            const taskTitle = input.value.trim();
            const column = input.closest('.todo-column');
            const statusId = getStatusIdFromColumn(column);
             try {
              const assignedTask = await addTask(taskTitle, statusId);
              const newTodo = document.createElement('div');
              newTodo.className = 'todo-item';
              newTodo.draggable = true;
              newTodo.textContent = taskTitle;
              newTodo.dataset.taskId = assignedTask.id; // Store new assigned task ID
              const itemsContainer = input.previousElementSibling;
              itemsContainer.appendChild(newTodo);
              setupDragAndDrop(newTodo);
              input.value = '';
              loadTasks();
          } catch (error) {
            console.error('Failed to add new task:', error);
        }
      }
    });
  });

    async function addTask(taskTitle, statusId) {
       try{
            const response = await fetch('/assigned-tasks/addAssignedTask/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ task_title: taskTitle, status_id: statusId})
            });
            if (!response.ok) {
              throw new Error(`Failed to add task. Status: ${response.status}`);
            }
            return await response.json();
       } catch (error) {
           console.error('Error adding task:', error);
           throw error; // rethrow
        }
    }

    function removeAllTodoItems() {
      const todoItems = document.querySelectorAll('div.todo-item');

      todoItems.forEach(item => {
        item.remove();
      });
    }

    loadTasks();
  });