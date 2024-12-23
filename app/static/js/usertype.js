async function getUserTypes() {
    const response = await fetch("/usertype/list", {
        method: "GET",
        headers: {"Accept": "application/json"}
    });
    if (response.ok === true) {
        const usertypes = await response.json();
        const rows = document.querySelector("tbody");
        usertypes.forEach(usertype => rows.append(row(usertype)));
    }
}

async function getUserType(id) {
    const response = await fetch(`/usertype/type/${id}`, {
        method: "GET",
        headers: {"Accept": "application/json"}
    });
    if (response.ok === true) {
        const usertype = await response.json();
        document.getElementById("userTypeId").value = usertype.id;
        document.getElementById("userType").value = usertype.usertype;
    } else {
        // если произошла ошибка, получаем сообщение об ошибке
        const error = await response.json();
        console.log(error.message); // и выводим его на консоль
    }
}

async function createUserType(userType) {
    const response = await fetch("/usertype/addUserType", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            usertype: userType
        })
    });
    if (response.ok === true) {
        const usertype = await response.json();
        document.querySelector("tbody").append(row(usertype));
    } else {
        const error = await response.json();
        console.log(error.message);
    }
}

async function editUserType(userTypeId, userType) {
    const response = await fetch(`/usertype/updateUserType/${userTypeId}`, {
        method: "PUT",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            //id: userTypeId,
            usertype: userType
        })
    });
    if (response.ok === true) {
        const usertype = await response.json();
        document.querySelector(`tr[data-rowid='${usertype.id}']`).replaceWith(row(usertype));
    } else {
        const error = await response.json();
        console.log(error.message);
    }
}

async function deleteUserType(id) {
    const response = await fetch(`/usertype/deleteUserType/${id}`, {
        method: "DELETE",
        headers: {"Accept": "application/json"}
    });
    if (response.ok === true) {
        const usertype = await response.json();
        document.querySelector(`tr[data-rowid='${usertype.id}']`).remove();
    } else {
        const error = await response.json();
        console.log(error.message);
    }
}

function reset() {
    document.getElementById("userTypeId").value = "";
    document.getElementById("userType").value = "";
}


function row(usertype) {

    const tr = document.createElement("tr");
    tr.setAttribute("data-rowid", usertype.id);

    const usertypeTd = document.createElement("td");
    usertypeTd.append(usertype.usertype);
    tr.append(usertypeTd);

    const linksTd = document.createElement("td");

    const editLink = document.createElement("button");
    editLink.append("Изменить");
    editLink.addEventListener("click", async () => await getUserType(usertype.id));
    linksTd.append(editLink);

    const removeLink = document.createElement("button");
    removeLink.append("Удалить");
    removeLink.addEventListener("click", async () => await deleteUserType(usertype.id));

    linksTd.append(removeLink);
    tr.appendChild(linksTd);

    return tr;
}

document.getElementById('resetBtn').addEventListener("click", () => reset());

document.getElementById("saveBtn").addEventListener("click", async () => {
    const id = document.getElementById("userTypeId").value;
    const usertype = document.getElementById("userType").value;
    if (id === "")
        await createUserType(usertype);
    else
        await editUserType(id, usertype);
    reset();
});
