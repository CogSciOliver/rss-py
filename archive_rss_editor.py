import xml.etree.ElementTree as ET 
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
RSS_FILE = "rss.xml"

# Include common namespaces
NS = {
    'dc': 'http://purl.org/dc/elements/1.1/',
    'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'
}

def load_rss():
    tree = ET.parse(RSS_FILE)
    root = tree.getroot()
    channel = root.find('channel')
    items_data = []

    for item in channel.findall('item'):
        item_dict = {}
        for child in item:
            tag_name = child.tag
            # Handle attributes for enclosure and itunes:image
            if tag_name == 'enclosure':
                item_dict['enclosure_url'] = child.attrib.get('url', '')
                item_dict['enclosure_length'] = child.attrib.get('length', '')
                item_dict['enclosure_type'] = child.attrib.get('type', '')
            elif tag_name.endswith('image') and 'href' in child.attrib:
                item_dict['itunes:image'] = child.attrib.get('href', '')
            else:
                item_dict[tag_name] = child.text or ''
        items_data.append(item_dict)
    return tree, channel, items_data

@app.route("/")
def index():
    _, _, items = load_rss()
    return render_template("editor.html", items=list(enumerate(items)))

@app.route("/edit/<int:item_idx>", methods=["POST"])
def edit_item(item_idx):
    tree, channel, _ = load_rss()
    item = channel.findall('item')[item_idx]
    
    form = request.form
    for child in item:
        tag_name = child.tag
        if tag_name == 'enclosure':
            child.attrib['url'] = form.get('enclosure_url', child.attrib.get('url',''))
            child.attrib['length'] = form.get('enclosure_length', child.attrib.get('length',''))
            child.attrib['type'] = form.get('enclosure_type', child.attrib.get('type',''))
        elif tag_name.endswith('image') and 'href' in child.attrib:
            child.attrib['href'] = form.get('itunes:image', child.attrib.get('href',''))
        else:
            if tag_name in form:
                child.text = form[tag_name]
    tree.write(RSS_FILE, encoding="utf-8", xml_declaration=True)
    return redirect("/")

@app.route("/add_item")
def add_item_page():
    return render_template("add_item.html")

@app.route("/add", methods=["POST"])
def add_item():
    tree = ET.parse(RSS_FILE)
    channel = tree.find("channel")

    form = request.form
    new_item = ET.Element("item")

    # Basic text tags
    for field in ["title", "description", "link", "guid", "dc:creator", "pubDate"]:
        elem = ET.SubElement(new_item, field)
        elem.text = form.get(field, "")

    # Enclosure
    enclosure = ET.SubElement(new_item, "enclosure")
    enclosure.attrib['url'] = form.get("enclosure_url", "")
    enclosure.attrib['length'] = form.get("enclosure_length", "")
    enclosure.attrib['type'] = form.get("enclosure_type", "")

    # iTunes tags
    for field in ["itunes:summary", "itunes:explicit", "itunes:duration",
                  "itunes:season", "itunes:episode", "itunes:episodeType"]:
        elem = ET.SubElement(new_item, field)
        elem.text = form.get(field, "")

    # iTunes image
    image = ET.SubElement(new_item, "itunes:image")
    image.attrib['href'] = form.get("itunes:image", "")

    # ---- Safe insertion before the first <item> ----
    first_item_index = None
    for i, elem in enumerate(channel):
        # strip namespace if present
        tag_name = elem.tag.split("}")[-1]  # e.g., 'item' or 'image'
        if tag_name == "item":
            first_item_index = i
            break

    if first_item_index is not None:
        channel.insert(first_item_index, new_item)
    else:
        channel.append(new_item)  # fallback if no items exist yet

    # Save
    tree.write(RSS_FILE, encoding="utf-8", xml_declaration=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)