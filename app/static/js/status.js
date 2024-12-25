async function getStatusList() {
    const response = await fetch("/statuses/list", {
        method: "GET",
        headers: {"Accept": "application/json"}
    });
    if (response.ok === true) {

        const statuses = await response.json();
        alert(statuses);
        const rows = document.querySelector("tbody");
        statuses.forEach(statuss => rows.append(row(statuss)));
    }
}

async function getStatus(id) {
    const response = await fetch(`/statuses/status/${id}`, {
        method: "GET",
        headers: {"Accept": "application/json"}
    });
    if (response.ok === true) {
        const statuss = await response.json();
        document.getElementById("statusID").value = statuss.id;
        document.getElementById("Status").value = statuss.title;
    } else {
        // если произошла ошибка, получаем сообщение об ошибке
        const error = await response.json();
        console.log(error.message); // и выводим его на консоль
    }
}

async function createStatus(Status) {
    const response = await fetch("/statuses/addStatus", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title: Status
        })
    });
    if (response.ok === true) {
        const status = await response.json();
        document.querySelector("tbody").append(row(status));
    } else {
        const error = await response.json();
        console.log(error.message);
    }

}

async function editStatus(statusID, Status) {
    const response = await fetch(`/statuses/editStatus/${statusID}`, {
        method: "PUT",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            //id: statusID,
            title: Status
        })
    });
    if (response.ok === true) {
        const statuss = await response.json();
        document.querySelector(`tr[data-rowid='${statuss.id}']`).replaceWith(row(statuss));
    } else {
        const error = await response.json();
        console.log(error.message);
    }
}

async function deleteStatus(id) {
    const response = await fetch(`/statuses/deleteStatus/${id}`, {
        method: "DELETE",
        headers: {"Accept": "application/json"}
    });
    if (response.ok === true) {
        const statuss = await response.json();
        document.querySelector(`tr[data-rowid='${statuss.id}']`).remove();
    } else {
        const error = await response.json();
        console.log(error.message);
    }
}

function reset() {
    document.getElementById("statusID").value = "";
    document.getElementById("Status").value = "";
}


function row(statuss) {

    const tr = document.createElement("tr");
    tr.setAttribute("data-rowid", statuss.id);

    const StatusTd = document.createElement("td");
    StatusTd.append(statuss.title);
    tr.append(StatusTd);

    const linksTd = document.createElement("td");

    const editLink = document.createElement("button");
    editLink.append("Изменить");
    editLink.addEventListener("click", async () => await getStatus(statuss.id));
    linksTd.append(editLink);

    const removeLink = document.createElement("button");
    removeLink.append("Удалить");
    removeLink.addEventListener("click", async () => await deleteStatus(statuss.id));

    linksTd.append(removeLink);
    tr.appendChild(linksTd);

    return tr;
}

document.getElementById('resetBtn').addEventListener("click", () => reset());

document.getElementById("saveBtn").addEventListener("click", async () => {
    const id = document.getElementById("statusID").value;
    const title = document.getElementById("Status").value;
    if (id === "")
        await createStatus(title);
    else
        await editStatus(id, title);
    reset();
});

getStatusList();
