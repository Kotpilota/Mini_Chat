async function getTasksList() {
    const response = await fetch("/tasks/list", {
        method: "GET",
        headers: {"Accept": "application/json"}
    });
    if (response.ok === true) {

        const tasks = await response.json();
        alert(tasks);
        const rows = document.querySelector("tbody");
        tasks.forEach(task => rows.append(row(task)));
    }
}

async function getTask(id) {
    const response = await fetch(`/tasks/task/${id}`, {
        method: "GET",
        headers: {"Accept": "application/json"}
    });
    if (response.ok === true) {
        const task = await response.json();
        document.getElementById("taskId").value = task.id;
        document.getElementById("title").value = task.title;
        document.getElementById("description").value = task.description;
    } else {
        // если произошла ошибка, получаем сообщение об ошибке
        const error = await response.json();
        console.log(error.message); // и выводим его на консоль
    }
}

async function createTask(title, description) {
    const response = await fetch("/tasks/addTask", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title: title,
            description: description
        })
    });
    if (response.ok === true) {
        const task = await response.json();
        document.querySelector("tbody").append(row(task));
    } else {
        const error = await response.json();
        console.log(error.message);
    }

}

async function editTask(taskId, title, description) {
    const response = await fetch(`/tasks/editTask/${taskId}`, {
        method: "PUT",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            //id: taskId,
            title: title,
            description: description
        })
    });
    if (response.ok === true) {
        const task = await response.json();
        document.querySelector(`tr[data-rowid='${task.id}']`).replaceWith(row(task));
    } else {
        const error = await response.json();
        console.log(error.message);
    }
}

async function deleteTask(id) {
    const response = await fetch(`/tasks/deleteTask/${id}`, {
        method: "DELETE",
        headers: {"Accept": "application/json"}
    });
    if (response.ok === true) {
        const task = await response.json();
        document.querySelector(`tr[data-rowid='${task.id}']`).remove();
    } else {
        const error = await response.json();
        console.log(error.message);
    }
}

function reset() {
    document.getElementById("taskId").value = "";
    document.getElementById("title").value = "";
    document.getElementById("description").value = "";
}


function row(task) {

    const tr = document.createElement("tr");
    tr.setAttribute("data-rowid", task.id);

    const taskTd = document.createElement("td");
    const taskTitle = document.createElement("div");
    const taskDescription = document.createElement("div");
    taskTitle.append(task.title);
    taskDescription.append(task.description);
    taskTd.append(taskTitle);
    taskTd.append(taskDescription);
    tr.append(taskTd);

    const linksTd = document.createElement("td");

    const editLink = document.createElement("button");
    editLink.append("Изменить");
    editLink.addEventListener("click", async () => await getTask(task.id));
    linksTd.append(editLink);

    const removeLink = document.createElement("button");
    removeLink.append("Удалить");
    removeLink.addEventListener("click", async () => await deleteTask(task.id));

    linksTd.append(removeLink);
    tr.appendChild(linksTd);

    return tr;
}

document.getElementById('resetBtn').addEventListener("click", () => reset());

document.getElementById("saveBtn").addEventListener("click", async () => {
    const id = document.getElementById("taskId").value;
    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;

    if (id === "")
        await createTask(title, description);
    else
        await editTask(id, title, description);
    reset();
});

getTasksList();
