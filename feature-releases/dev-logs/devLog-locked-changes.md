
 Last Updated 03.02.2026 - Author: Danii Oliver, Software Engineer 

 ## Locked Change Feature Overview
 The Locked Changes feature is designed to add an extra layer of confirmation before allowing users to edit input fields or delete items in the RSS Editor. This helps prevent accidental changes or deletions by requiring users to type specific keywords to confirm their actions.

 ## Features
 1. **Attempt Change**: When a user tries to edit a locked input field, they will be prompted to type "CHANGE" exactly. If they enter the correct keyword, the input field will become editable. If they enter an incorrect keyword or cancel the prompt, the field remains read-only.

 2. **Attempt Delete**: When a user tries to delete an item, they will be prompted to type "DELETE" exactly. If they enter the correct keyword, the deletion will proceed. If they enter an incorrect keyword or cancel the prompt, the item will not be deleted.

 ## Usage
 1. To enable editing of a locked input field:
    - Click on the input field you wish to edit.
    - A prompt will appear asking you to type "CHANGE".
    - Type "CHANGE" exactly and click OK to enable the input field for editing.

 2. To delete an item:
    - Click on the delete button next to the item you wish to delete.
    - A prompt will appear asking you to type "DELETE" along with the item name for confirmation.
    - Type "DELETE" exactly and click OK to confirm deletion.

 ## Implementation
 The Locked Changes feature is implemented in the `locked-changes.js` file, which is linked in the `editor.html` template. The JavaScript functions handle the prompts and actions based on user input.

 ## Conclusion
 This feature enhances the user experience by adding a safeguard against unintended edits and deletions, ensuring that users are fully aware of their actions before they proceed.       

### The attemptDelete & attemptChange features. What I did was add a JavaScript file called locked-changes.js and linked it in the editor.html. In this file, I created two functions: attemptChange() and attemptDelete(idx, title).     
 These features will prompt the user to type specific keywords ("CHANGE" for enabling the input field and "DELETE" for confirming deletion) before allowing the respective actions to proceed. This adds an extra layer of confirmation to prevent accidental changes or deletions.
let's draft a readme for this feature as well, to explain how it works and how to use it.

```
function attemptChange() {
    var confirmation = prompt("To enable this input field, please type 'CHANGE' exactly:");

    if (confirmation === "CHANGE") {
         If the user types "CHANGE", remove the readonly attribute
        document.getElementById("imgUrlInput").removeAttribute("readonly");
        alert("Input field is now enabled for editing.");
    } else {
         If the input is incorrect or cancelled, the field remains readonly
        alert("Incorrect input. The field remains read-only.");
    }
}

function attemptDelete(idx, title) {
    var delConfirmation = prompt("To confirm deletion of this entry name: " + title + ", please type 'DELETE' exactly:");
    alert("you are about to delete this entry name: " + title);

    if (delConfirmation === "DELETE") {
         If the user types "DELETE", remove confirmation and proceed with deletion
        var form = document.createElement("form");
        form.method = "post";
        form.action = "/delete/" + idx;
        document.body.appendChild(form);
        form.submit();
    } else {
         If the input is incorrect or cancelled, the field remains readonly
        alert("Incorrect input. Item will not be deleted.");
    }

}
```
I needed to pass idx to the JavaScript function. What I did was pass the `idx` value to the `attemptDelete(idx, title)` function so that it can correctly identify which item to delete when the form is submitted. You can do this by modifying the onclick event in your HTML to include the `idx` as an argument. Here's how you can do it:

 In the HTML (editor.html), update the delete button to pass the `idx` value to the `attemptDelete(idx, title)` function: 
 now let's work on the delete button, we want to add a confirmation prompt before the deletion is processed. We can use a similar approach to the change confirmation, but with a different keyword for confirmation. Here's how you can implement it:

 1. Add an onclick event to the delete button that calls a JavaScript function to handle the confirmation.
 2. In the JavaScript function, prompt the user to type a specific keyword (e.g., "DELETE") to confirm the deletion.
 3. If the user types the correct keyword, proceed with the deletion by submitting the form. If not, cancel the deletion.

 Here's how you can modify your HTML and JavaScript:

 In your HTML (editor.html), update the delete button to call the `attemptDelete()` function:    
 ```    
 {# <form method="post" action="/delete/{{ idx }}" style="display: inline"> #}
 <form style="display: inline"> {# REMOVE THE FORM WRAPPER #}
     <button class="delete-button" type="submit" onclick="attemptDelete({{ idx }}, '{{ item.get('title', 'Unknown') }}')">&#x2715; &nbsp; Delete Item {{ item.get('title', 'Unknown') }}</button>
 </form> {# REMOVE THE FORM WRAPPER #}
```
 In your JavaScript (locked-changes.js), add the `attemptDelete()` function:
```
 function attemptDelete(idx, title) {
     var delConfirmation = prompt("To confirm deletion of this entry name: " + title + ", please type 'DELETE' exactly:");
     alert("you are about to delete this entry name: {{ item.get('title', 'Unknown') }} ");

     if (delConfirmation === "DELETE") {
          If the user types "DELETE", remove confirmation and proceed with deletion
         method="post" action="/delete/{{ idx }}"
         alert("Item deleted successfully.");
     } else {
          If the input is incorrect or cancelled, the field remains readonly
         alert("Incorrect input. Item will not be deleted.");
     }

 }
```
 Make sure to replace the placeholder values in the JavaScript function with the actual values from your template context. This way, when a user clicks the delete button, they will be prompted to confirm their action, and only if they type "DELETE" will the deletion proceed. 


 
{# decoupled the delete confirmation call for dynamic confirmation then action #}

{# I need to add a confirmation step to change the img URL. I want to make sure that the user is aware that they are changing the image URL and that it will affect the feed's appearance. I will add a JavaScript function that prompts the user for confirmation before allowing them to change the image URL. If they confirm, the change will be made; if they cancel, the input will remain unchanged.
First I need to identify the input field for the image URL in the HTML form and add the attribute readonly. Once I have that, I can add an event listener to that input field that triggers a confirmation dialog when the user tries to change the value. If the user confirms, the change will be allowed by js removing the readonly attribute and highlighting to indicate the input field is being edited; if they cancel, the input will remain unchanged and the readonly attribute will stay in place. This way, the user is explicitly aware that they are making a change to the image URL and can make an informed decision about whether to proceed or not.

how do I add this feature to the dynamic form?To add a confirmation step for changing the image URL in your dynamic form, you can follow these steps:	
1. Identify the input field for the image URL in your HTML form. It might look something like this:
No imputs are hardcded in the template, so you will need to add a condition to check if the current field is the image URL field. For example, if your image URL field is named "image_url", you can modify your template like this:
```html
{% if field == "image_url" %}
<input type="text" id="{{ field }}_input_{{ idx }}" name="{{ field }}" value="{{ value }}" readonly />
{% else %}
<input type="text" id="{{ field }}_input_{{ idx }}" name="{{ field }}" value="{{ value }}" />
{% endif %}
```
2. Add a JavaScript function that listens for changes to the image URL input field and prompts the user for confirmation. You can add this function in your existing `locked-changes.js` file:
```javascriptdocument.addEventListener("DOMContentLoaded", function() {
	const imageUrlInputs = document.querySelectorAll("input[name='image_url']");
	imageUrlInputs.forEach(function(input) {
		input.addEventListener("click", function() {
			if (input.hasAttribute("readonly")) {
				const confirmChange = confirm("Are you sure you want to change the image URL? This will affect how your feed appears.");
				if (confirmChange) {
					input.removeAttribute("readonly");
					input.style.backgroundColor = "#ffdddd"; // Highlight the input to indicate it's being edited
				} else {
					// If the user cancels, keep the input readonly and unchanged
					input.value = input.getAttribute("value"); // Reset to original value
				}
			}
		});
	});
});
```
3. Make sure to include the `locked-changes.js` script in your HTML template if it's not already included:
```html<script src="{{ url_for('static', filename='locked-changes.js') }}"></script>
```	 #}


{# TECHNICAL EDITS & SKILLS #}
{# building string concatenations to target element ids based on field and index with unique identifiers like {{ field }}_box_{{ idx }}	 or 	_preview or _input to add dynamic functionality such as locked changes that are readonly and can be unlocked and UI indicators that changes to protected fields are being made.  #}


final

// JavaScript for handling locked input fields and delete confirmations
//locked-changes.js

function attemptChange(input, previewBox) {
    var confirmation = prompt("To enable this input field, please type 'CHANGE' exactly:");
    alert( "id= " + input);

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
