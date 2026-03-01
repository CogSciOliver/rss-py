function attemptChange() {
    var confirmation = prompt("To enable this input field, please type 'CHANGE' exactly:");

    if (confirmation === "CHANGE") {
        // If the user types "CHANGE", remove the readonly attribute
        document.getElementById("targetInput").removeAttribute("readonly");
        alert("Input field is now enabled for editing.");
    } else {
        // If the input is incorrect or cancelled, the field remains readonly
        alert("Incorrect input. The field remains read-only.");
    }
}