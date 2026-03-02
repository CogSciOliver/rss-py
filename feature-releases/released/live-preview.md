# Architecture Notes — Live Preview System

**Last Updated:** 03.02.2026
**Author:** Danii Oliver, Software Engineer
* * * * *

## Design Philosophy

The live preview feature was intentionally designed to be:

- **Decoupled from backend logic**
- **Convention-driven instead of configuration-driven**
- **Scalable without modification**
- **Easy to reason about during debugging**

Rather than passing structured item data from Flask into JavaScript, the system relies on predictable DOM naming conventions.

This removes tight coupling between server-rendered data structures and frontend behavior.

---

## Separation of Concerns

### Backend (Flask + Jinja):

- Renders form inputs and preview spans
- Applies a deterministic ID naming pattern:

   `id="idpattern"`

   `{field}_input_{index}`
   `{field}_preview_{index}`

````

### Frontend (JavaScript):

- Discovers inputs dynamically using attribute selectors
- Derives preview IDs using string transformation
- Attaches listeners without knowledge of item structure

The frontend does not need:

- Item arrays
- Field lists
- Explicit mapping configuration

This ensures UI behavior remains stable even if:

- New RSS fields are added
- Field order changes
- Items are inserted or removed
---

## Why Convention Over Configuration?

Instead of:
* Passing JSON objects to JS
* Looping through field definitions
* Hardcoding ID references
The system uses:
```id="strategy"```
to derive corresponding preview IDs with simple string replacement:
```this.id.replace("_input_", "_preview_")```.
This convention-based mapping:
* Reduces cognitive overhead  Eliminates redundant state Prevents synchronization bugs Keeps JavaScript extremely lightweight.
---
## Performance Characteristics
*
* Event listeners are attached once on `DOMContentLoaded`
* Only elements matching `[id*='_input_']` are targeted
* Updates use direct `textContent` assignment
* No re-rendering, no DOM rebuilding
*
The system operates in O(n) initialization time relative to input count, with constant-time update per keystroke.
---
## Maintainability Considerations
This design supports:
* Adding new editable fields without JS changes
* Refactoring backend models without breaking preview logic
* Debugging by inspecting ID relationships directly in the DOM
There is no hidden state layer or intermediate abstraction.
The DOM itself is the source of truth.
---
## Alternative Approaches Considered| Approach | Why It Was Not Used |
| --- | --- |
| Passing serialized items to JS | Tight coupling with backend model |
| Field-by-field manual wiring | Not scalable |
| Frontend framework (React/Vue) | Overkill for current scope |
| Two-way binding library | Adds unnecessary complexity |
 The chosen solution provides 90% of the benefit with minimal complexity.
---
## Extensibility Path
 Future enhancements could include:
 * Change tracking indicators
 * Debounced input updates
 * Dirty state detection
 * Undo support
 * Field-level validation feedback
 * Transition animations on update
 All without restructuring the current system.
---
## Summary
 This implementation demonstrates:
 * Controlled complexity
 * Intentional decoupling
 * Scalable naming conventions
 * Practical DOM-driven architecture
 It is optimized for clarity, extensibility, and interview-ready discussion.
---
r If you'd like, I can now generate:
 • A short executive summary version
 • A “Lessons Learned” section
 • Or a diagram-style explanation for visual documentation
 Your choice.
````
