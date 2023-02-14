function selectColor(button) {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", document.URL + '/color/' + button.innerHTML);
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.send()

    xhr.onload = () => {
        if (xhr.status == 200) {
            console.log(xhr.responseText);
        }
    };
}

function setColor(stateAcronym) {
    
}