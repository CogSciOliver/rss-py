{# jump to name or date or season# & epi# or guid or url #}
{# option to search if not known based on keywords in the description or summary #}




**Last Updated 03.03.2026**

# Get Item Count 
!Part of the the Jump-To Feature 
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

# Eval Item_Count - IDX 
Edit both the episode number and the indexed id 

{# Note Episode number is == item count - idx
if idx == 80 and item count == 84 then "Episode 4" is 84 - 80  
eval item count - idx # 
then jump to id=#episode #}

```
<h2 id="{{ item_count - idx }}">Edit Episode # {{ item_count - idx }}: {{ item.get('title', 'Unknown Title') }}</h2>
```

Fixed with 
```
    items_enum = []
    for idx, item in enumerate(items):
        episode_number = item_count - idx
        items_enum.append((idx, item, episode_number))
    
```

```
<h2>Episode List</h2>
		{% for idx, item, episode_number in items %}
		<a class="outline-link" href="#{{ episode_number }}">Episode # {{ episode_number }}: {{ item.get('title', 'Unknown Title') }}</a>
		{% endfor %}	

		{% for idx, item, episode_number in items %}
		<form method="post" action="/edit/{{ idx }}">
			<div class="edit-section">
				<h2 id="{{episode_number}}">Edit Episode {{ episode_number }}: {{ item.get('title', 'Unknown Title') }}</h2>
				<table class="edit-table">
                <!-- Continue Code -->
```

## Now have a list and links to jump to 
```
{% for idx, item, episode_number in items %}
<a class="outline-link" href="#{{ episode_number }}">
    Episode # {{ episode_number }}: {{ item.get('title', 'Unknown Title') }}
</a>
{% endfor %}
```

## control display order/sorting


**notes**
Now have a list and links to jump to
NEW FEATURE RELEASE: "Jump To Item" only one part of jump to with id number no dynamics yet  v26.03.02-04:43