function analyzeGuess(json_response) {
    var play_status = document.getElementById("play_status")
    var outcome = json_response.outcome;
    var game = json_response.game;
    var analysis = outcome.analysis;
    var status = game.status;

    if (status == "won" || status == "lost") {
        play_status.innerHTML = outcome.status;
        if (analysis == undefined || analysis == '') {
            return;
        }
    } else {
        play_status.innerHTML = outcome.status;
    }

    for (var i = 0; i < g_digits; i++) {
        var outfield = document.getElementById('row_' + (g_try - 1)  + '_col_'+i);
        outfield.innerHTML = analysis[i].digit;
        outfield.className = "miss"
        if (analysis[i].match) {
            outfield.className += " bull "
        } else if (analysis[i].in_word) {
            outfield.className += " cow "
        }
        if (analysis[i].multiple) {outfield.className += " multiple "}
    }
/*    alert(json_response.outcome.bulls + ' bulls and ' + json_response.outcome.cows + ' cows.'); */
}

function parseToJSON(text) {
    var jsonResponse = {};
    try {
        jsonResponse = JSON.parse(' ' + text + ' ');
    }
    catch(err) {
        console.log('Error: ' + err);
        console.log('Input text was: ' + text);
    }
    return jsonResponse;
}

function parseResponse(text) {
    var start=text.indexOf("{")
    var end=text.indexOf("}") + 1
    return text.substring(start, end)
}

function makeGuess() {
    var play_status = document.getElementById("play_status");
    play_status.innerHTML = "Connecting to game server. Please wait...";

    /* Build digits */
    let list_of_guesses = [];
    for (var dig = 0; dig < g_digits; dig++) {
        let digit = document.getElementById('digit_'+dig);
        list_of_guesses.push(digit.value);
    }
    let params = {
        key: g_key,
        digits: list_of_guesses
    }

    /* Make a guess */
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        var json_response = {};

        if (this.readyState == 4) {
            if (this.status == 200) {
                g_try++;
                console.log('Success. Processing game response ' + this.responseText);
                json_response = parseToJSON(this.responseText);
                analyzeGuess(json_response);
            }
            else if (this.status == 400) {
                json_response = parseToJSON(this.responseText);
                play_status.innerHTML = json_response.exception;
            }
            else {
                json_response = parseToJSON(this.responseText);
                play_status.innerHTML = "An error occurred: " + json_response.exception;
                console.log('An error occurred: ' + this.responseText);
            }
        }
    };

    xhttp.open("PUT", window.location.href, true)
    xhttp.setRequestHeader("Content-Type", "application/json")
    xhttp.send(JSON.stringify(params), "json")
}
