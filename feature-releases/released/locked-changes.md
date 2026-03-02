**project presentation case study that you can use for:**
- Feature README
- Portfolio
- Code review presentation
- Technical interview walkthrough
- Internal UI documentation

# Locked Changes Feature 🔐 

**Last Updated:** 03.02.2026
**Author:** Danii Oliver, Software Engineer
* * * * *
## Project Context

The RSS Editor allows users to modify and delete feed items dynamically. While functional, this introduces risk:
- Accidental edits to critical metadata
- Accidental deletions
- Unintended feed-breaking changes
The **Locked Changes Feature** introduces intentional friction for sensitive operations without complicating backend logic.

## Problem Statement

Standard confirmation dialogs (`confirm()`) are too easy to dismiss.
Users can accidentally:
- Modify protected fields (e.g., image URL, dc:creator)
- Delete feed items
- Alter namespaced metadata that impacts downstream feed consumers

We needed:
- Stronger confirmation
- Zero backend restructuring
- Clean separation of concerns
- Fully decoupled frontend logic

## Solution Overview
A lightweight JavaScript protection layer that:
1. Requires typing `"CHANGE"` to unlock protected fields
2. Requires typing `"DELETE"` to confirm deletion
3. Dynamically targets inputs using generated IDs
4. Preserves backend route separation
All logic is isolated inside:
static/locked-changes.js
No route merging. No backend coupling.

## Architecture
### Backend (Flask)

Routes remain clean and separate:
/edit/<int:item_index>\
/delete/<int:item_index>
No additional backend logic required.
Deletion is triggered dynamically via a JS-generated POST form.

### Frontend (Dynamic Template)

Inputs are generated dynamically using:
id="{{ field }}_input_{{ idx }}"\
id="{{ field }}_preview_{{ idx }}"
This enables:
- Unique field targeting
- Dynamic JS manipulation
- Field-specific UI effects
- Namespaced RSS support (`itunes:*`, `dc:*`)

## Feature 1: Attempt Change

### Goal
Protect sensitive fields (e.g., image URL) from accidental edits.
### Flow
1. Field is rendered as `readonly`
2. User clicks field
3. Prompt appears:
 Type CHANGE exactly
4. If correct:
 - `readonly` removed
 - Field visually highlighted
5. If incorrect:
 - Field remains locked

## Implementation
### HTML (Dynamic Template Logic)
Target for previewBox
```
<td id="{{field}}_previewBox_{{idx}}">
```
```
{% elif field == "itunes:image" or field == "dc:creator" %}
<input 
    style="margin-bottom: 10px;" 
    type="text" id="{{ field }}_input_{{ idx }}" 
    name="{{ field }}" 
    value="{{ value }}" 
    readonly
    aria-readonly />
							
<button 
    type="button" 
    class="outline-button" 
    onclick="attemptChange('{{ field }}_input_{{ idx }}', '{{ field }}_previewBox_{{ idx }}')"> 
    &#9888;&nbsp;Change This Protected Field
</button>
{% endif %}
```

### JavaScript
```
function attemptChange(input, previewBox) {
 var confirmation = prompt(\
 "To enable this input field, please type 'CHANGE' exactly:"\
 );
 if (confirmation  "CHANGE") {\
 document.getElementById(input).removeAttribute("readonly");\
 document.getElementById(input).removeAttribute("aria-readonly");
 document.getElementById(previewBox).style.backgroundColor = "#ffdddd";
 alert("Input field is now enabled for editing.");\
 } else {\
 alert("Incorrect input. The field remains read-only.");\
 }\
}
```
## Feature 2: Attempt Delete

### Goal
Prevent accidental feed item deletion.
### Flow
1. User clicks Delete
2. Prompt appears:
 Type DELETE exactly
3. If correct:
 - JS dynamically creates a POST form
 - Submits to `/delete/<idx>`
4. If incorrect:
 - No action taken

## Implementation

### HTML
```
<button
 type="button"
 class="delete-button"
 onclick="attemptDelete({{ idx }}, '{{ item.get('title', 'Unknown') }}')">
 &#x2715; Delete Item {{ item.get('title', 'Unknown') }}
</button>
```

### JavaScript
```
function attemptDelete(idx, title) {
 var delConfirmation = prompt(
 "To confirm deletion of: \"" + title +\
 "\"\nPlease type DELETE exactly:"
 );
 if (delConfirmation  "DELETE") {
 var form = document.createElement("form");
 form.method = "post";
 form.action = "/delete/" + idx;
 document.body.appendChild(form);
 form.submit();
 alert("You are about to delete the entry named: " + title);
 } else {
 alert("Incorrect input. Item will not be deleted.");
 }
}
```

## Engineering Decisions

### 1. Decoupled Code Logic
All confirmation logic lives in:
locked-changes.js
Backend routes remain untouched.

### 2. Dynamic ID Construction
Using:
{{ field }}_input_{{ idx }}\
{{ field }}_previewBox_{{ idx }}

Enabled:
- Scalable field targeting
- Namespace-safe manipulation
- No hardcoded inputs
- Support for arbitrary RSS metadata fields

### 3. Preventing Default Form Submission
Delete buttons use:
type="button"
JS manually creates and submits the POST form.
This prevents premature submission before confirmation.

## Software UX Considerations

### Why not just `confirm()`?
Because:
- Confirm dialogs are reflex-dismissed.
- Typed confirmation forces intentional action.
- Creates deliberate pause before destructive operations.
- Protects feed integrity.

### Risk Mitigation

This feature protects against:
- Accidental deletion
- Editing of protected fields
- Feed corruption via namespace-sensitive tags
- Image URL misconfiguration affecting feed preview clients

## Skills Demonstrated

- DOM manipulation
- Dynamic ID construction
- Event-driven architecture
- Decoupled frontend design
- Safe destructive action patterns
- Template-driven JS integration
- Namespaced XML awareness
- Route separation for maintainability

## Future Enhancements

Potential upgrades:
- Replace `prompt()` with modal dialog
- Add undo-delete timer
- Add per-field lock icon indicator
- Add field-level change tracking
- Add soft-delete before permanent removal

## Conclusion

The Locked Changes Feature introduces intentional friction for sensitive operations without increasing backend complexity.
It demonstrates:
- Controlled UI design
- Clean architecture
- Separation of concerns
- Thoughtful UX engineering
- Production-aware defensive programming
This feature transforms **rss_editor.py** a functional python editor into a protected editing environment.
