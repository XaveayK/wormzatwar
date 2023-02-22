/*function selectColor(button) {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", document.URL + '/color/' + button.innerHTML);
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.send()

    xhr.onload = () => {
        if (xhr.status == 200) {
            console.log(xhr.responseText);
        }
    };
}*/

function startGame(){
    let xhr = new XMLHttpRequest();
    xhr.open("POST", document.URL + '/startGame');
    xhr.setRequestHeader("X-CSRFToken", csrftoken);

    xhr.onload = () => {
        if (xhr.status == 200) {
            document.getElementById("start").style.display="none"
        }
    }
    
    xhr.send()
}

function hideRules() {
    document.getElementById("Overlap").style.display = "none";
    document.getElementById("ruleText").innerHTML = '';
}

function displayRules() {
    document.getElementById("Overlap").style.display="inline";
    document.getElementById("ruleText").innerHTML = `1. Selecting an initial country is decided upon randomly for each user by computer when start button clicked.<br>
    2. Invading a country requires more troops in adjacent countries than are in the current country.<br>
    3. Certain countries produce troops with advantages to invading or protection from being invaded. These will be listed. <br>
    4. Non-Flying units can traverse 1 (One) country per turn, or 3 (Three) turns to traverse the Atlantic and Pacific.<br>
    5. Flying units can traverse 3 (Three) countries per turn or 1 (One) turn to traverse the Atlantic and Pacific.<br>
    6. Countries produce a certain amount of food per turn excess for troops, if the troop count becomes more than <br>
    can be sustained by that country, lose troops per turn in that country.<br>
    7. Movement of food between countries occurs at the same rate as non-flight units.<br>
    8. All players turns occur simultaneously and the action of that turn occurs once everyone has clicked ready.<br>
    9. Precedent is given to defensive plays, where moving troops within occupied territory happens first.<br>
    10. If no countries left, user loses and is removed from game. If only one user left, that user wins.`;
}

function bootOperations() {

    // Sets a default of self for displaying countries occupied
    var userName = document.getElementById("countryList").children[0].innerHTML;
    displayOccupied(userName);
    console.log("It's finished function call");


    /*let xhr = new XMLHttpRequest();
    xhr.open("GET", document.URL + "/status");

    xhr.onload = () => {
        console.log("What the fuckl");
        console.log(xhr.responseText);
    };*/
}

function getUserForDisplay(user) {
    userName = user.innerHTML;
    displayOccupied(userName);
}

function displayOccupied(user) {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/get-occupiers");
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    let data = `{"Username":"${user}","LobbyID":"${document.getElementById("lobbyPK").getAttribute("value")}"}`;

    xhr.onload = () => {
        var parentNode = document.getElementById("countryList");
        parentNode.innerHTML = ''; //Lazy way because there isn't an attachment to event handlers
        createListNodeForCountry(user, parentNode);
        var countries = JSON.parse(xhr.responseText);
        for (country in countries["States"]) {
            createListNodeForCountry(countries["States"][country], parentNode);
        }
    }
    xhr.send(data);
    return
}

function createListNodeForCountry(text, parentNode) {
    const node = document.createElement("li");
    node.appendChild(document.createTextNode(text));
    parentNode.appendChild(node);
}

function setOwner(stateAcronym) {
    
}