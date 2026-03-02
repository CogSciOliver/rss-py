// JavaScript for handling locked input fields and delete confirmations
//locked-changes.js

function attemptChange(input, previewBox, lockIcon) {
    var confirmation = prompt("To enable this input field, please type 'CHANGE' exactly:");

    if (confirmation === "CHANGE") {
        // If the user types "CHANGE", remove the readonly attribute and the lock
        document.getElementById(input).removeAttribute("readonly"); 
        document.getElementById(input).removeAttribute("aria-readonly"); 
        document.getElementById(lockIcon).style.display = "none"; // Hide the lock icon
        document.getElementById(previewBox).style.backgroundColor = "#ffdddd"; // Highlight the input to indicate it's being edited
        document.getElementById(previewBox).style.border = "2px solid #ff0000"; // Add a red border to indicate it's being edited
        

        alert("Input field is now enabled for editing.");
    } else {
        // If the input is incorrect or cancelled, the field remains readonly
        alert("Incorrect input. The field remains read-only.");
    }
}

function attemptDelete(idx, title) {
    var delConfirmation = prompt("To confirm deletion of: \"" + title +"\"\nPlease type DELETE exactly:"); 

    if (delConfirmation === "DELETE") {
        // If the user types "DELETE", remove confirmation and proceed with deletion
        var form = document.createElement("form");
        form.method = "post";
        form.action = "/delete/" + idx;
        document.body.appendChild(form);
        form.submit();
        alert("You are about to delete the entry named: " + title);
    } else {
        // If the input is incorrect or cancelled, the field remains readonly
        alert("Incorrect input. Item will not be deleted.");
    }

}