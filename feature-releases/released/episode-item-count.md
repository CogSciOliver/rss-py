    **Last Updated 03.03.2026**

# !Part of the the Jump-To Feature 
## This is only the display part of the dynamic search/jump feature

Displays the item count by passing it from the Flask route to the template and rendering it somewhere at the top/side of the editor page. 

## Implementation:

1. Update the Python Flask route (/) to include the item count:
```
@app.route("/")
def index():
    tree, channel, items = load_rss()
    items_enum = list(enumerate(items))
    item_count = len(items)  # count of RSS items
    return render_template("editor.html", items=items_enum, item_count=item_count)
```

2. Display it on the HTML template (editor.html):
```
<h2>Edit Existing Items</h2>
<p>Total RSS items: {{ item_count }}</p>

{% for idx, item in items %}
<form method="post" action="/edit/{{ idx }}">
    <!--  existing table and fields here -->
</form>
<hr />
{% endfor %}
```