function sendMessage() {
    var userInput = document.getElementById("user-input").value;
    if (userInput.trim() === "") return;

    var chatBox = document.getElementById("chat-box");

    chatBox.innerHTML += "<div class='user-message'>" + userInput + "</div><br>";

    setTimeout(function () {
        chatBox.innerHTML += "<div class='bot-message'>Bot: Hi, I'm a styled chat bot!</div><br>";
        chatBox.scrollTop = chatBox.scrollHeight;
    }, 500);

    document.getElementById("user-input").value = "";
}

document.getElementById("user-input").addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});
