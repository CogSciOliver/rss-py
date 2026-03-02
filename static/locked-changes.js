// JavaScript for handling locked input fields and delete confirmations
//locked-changes.js

function attemptChange(input, previewBox) {
    var confirmation = prompt("To enable this input field, please type 'CHANGE' exactly:");

    if (confirmation === "CHANGE") {
        // If the user types "CHANGE", remove the readonly attribute
        document.getElementById(input).removeAttribute("readonly"); 
        document.getElementById(input).removeAttribute("aria-readonly"); 
        document.getElementById(previewBox).style.backgroundColor = "#ffdddd"; // Highlight the input to indicate it's being edited
        //this needs to be updated to target the correct input field based on the idx parameter which can be concatenated with the field name to form the correct ID of the input element. 
        // For example, if the field is "itunes:image" and idx is 0, the ID would be "itunes:image_input_0". 
        //or it can have no concatenation if the idx is already included in the field name, so it would just be idx.

        // for document.getElementById(`_preview_${idx}`).style.backgroundColor = "#ffdddd"; 
        // it needs to target the correct preview element as well, which would be `_preview_${idx}` if the idx is included in the field name, or it would need to be updated to target the correct preview element based on the idx parameter.
        // the filed name can be extracted from the idx parameter by splitting it at the "_input_" substring and taking the first part, which would give the field name. Then the preview element can be targeted using that field name and the idx parameter to form the correct ID of the preview element, which would be `${field}_preview_${idx}`.

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