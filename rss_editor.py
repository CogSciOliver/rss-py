#import xml.etree.ElementTree as ET 
#DO NOT USE xml.etree.ElementTree as it does not support namespaces properly, which is crucial for handling RSS feeds with itunes and dc namespaces.

from flask import Flask, render_template, request, redirect, url_for
from lxml import etree as ET

app = Flask(__name__)
RSS_FILE = "rss.xml"

# Namespaces
NS = {
    'itunes': "http://www.itunes.com/dtds/podcast-1.0.dtd",
    'dc': "http://purl.org/dc/elements/1.1/"
}

# --- Load RSS and convert items to dicts for display ---
def load_rss():
    parser = ET.XMLParser(remove_blank_text=False)
    tree = ET.parse(RSS_FILE, parser)
    root = tree.getroot()
    channel = root.find("channel")
    items = []

    for item_elem in channel.findall("item"):
        item = {}
        for child in item_elem:
            tag = child.tag
            # Enclosure attributes
            if tag == "enclosure":
                item['enclosure_url'] = child.get('url', '')
                item['enclosure_length'] = child.get('length', '')
                item['enclosure_type'] = child.get('type', '')
            # iTunes namespaced tags
            elif tag == f"{{{NS['itunes']}}}image":
                item['itunes:image'] = child.get('href', '')
            elif tag.startswith(f"{{{NS['itunes']}}}"):
                item['itunes:' + tag.split('}')[1]] = child.text or ''
            # DC namespace
            elif tag.startswith(f"{{{NS['dc']}}}"):
                item['dc:' + tag.split('}')[1]] = child.text or ''
            else:
                item[tag] = child.text or ''
        items.append(item)

    return tree, channel, items

# --- Index page: show all items ---
@app.route("/")
def index():
    _, _, items = load_rss()
    return render_template("editor.html", items=list(enumerate(items)))

# --- Edit existing item ---
@app.route("/edit/<int:item_index>", methods=["GET", "POST"])
def edit_item(item_index):
    parser = ET.XMLParser(remove_blank_text=False)
    tree = ET.parse(RSS_FILE, parser)
    root = tree.getroot()
    channel = root.find("channel")
    items = channel.findall("item")
    item = items[item_index]

    if request.method == "POST":
        form = request.form

        # Standard RSS tags
        for field in ["title", "description", "link", "guid", "pubDate"]:
            elem = item.find(field)
            if elem is None:
                elem = ET.SubElement(item, field)
            elem.text = form.get(field, "")

        # DC creator
        dc_creator_tag = f"{{{NS['dc']}}}creator"
        elem = item.find(dc_creator_tag)
        if elem is None:
            elem = ET.SubElement(item, dc_creator_tag)
        elem.text = form.get("dc:creator", "")

        # Enclosure
        enclosure = item.find("enclosure")
        if enclosure is None:
            enclosure = ET.SubElement(item, "enclosure")
        enclosure.attrib['url'] = form.get("enclosure_url", "")
        enclosure.attrib['length'] = form.get("enclosure_length", "")
        enclosure.attrib['type'] = form.get("enclosure_type", "")

        # iTunes tags
        for field in ["summary", "explicit", "duration", "season", "episode", "episodeType"]:
            tag = f"{{{NS['itunes']}}}{field}"
            elem = item.find(tag)
            if elem is None:
                elem = ET.SubElement(item, tag)
            elem.text = form.get(f"itunes_{field}", "")

        # iTunes image
        tag = f"{{{NS['itunes']}}}image"
        image = item.find(tag)
        if image is None:
            image = ET.SubElement(item, tag)
        image.set("href", form.get("itunes_image", ""))

        # Save RSS
        tree.write(RSS_FILE, encoding="utf-8", xml_declaration=True, pretty_print=True)
        return redirect("/")

    return render_template("edit.html", item=item, index=item_index)

# --- Delete existing item function ---
@app.route("/delete/<int:item_index>", methods=["POST"])
def delete_item(item_index):
    parser = ET.XMLParser(remove_blank_text=True)
    tree = ET.parse(RSS_FILE, parser)
    root = tree.getroot()
    # Find the <channel> element (adjust namespace if needed)
    channel = root.find("channel") or root.find(".//{http://purl.org/rss/1.0/}channel")
    
    if channel is None:
        # Handle error: no channel found
        return redirect("/")

    # Get all <item> elements under channel (handle namespaces)
    items = channel.findall("item") or channel.findall(".//{http://purl.org/rss/1.0/}item")

    # Validate index
    if 0 <= item_index < len(items):
        item_to_delete = items[item_index]
        channel.remove(item_to_delete)  # Remove directly from channel
        tree.write(RSS_FILE, encoding="utf-8", xml_declaration=True, pretty_print=True)

    return redirect("/")

# --- Add new item page ---
@app.route("/add_item")
def add_item_page():
    return render_template("add_item.html")

# --- Add new item POST ---
@app.route("/add", methods=["GET", "POST"])
def add_item():
    if request.method == "POST":
        parser = ET.XMLParser(remove_blank_text=False)
        tree = ET.parse(RSS_FILE, parser)
        root = tree.getroot()
        channel = root.find("channel")
        form = request.form

        new_item = ET.Element("item")

        # Standard RSS tags
        for field in ["title", "description", "link", "guid", "pubDate"]:
            elem = ET.SubElement(new_item, field)
            elem.text = form.get(field, "")

        # DC creator
        dc_creator_tag = f"{{{NS['dc']}}}creator"
        elem = ET.SubElement(new_item, dc_creator_tag)
        elem.text = form.get("dc:creator", "")

        # Enclosure
        ET.SubElement(new_item, "enclosure",
                      url=form.get("enclosure_url", ""),
                      length=form.get("enclosure_length", ""),
                      type=form.get("enclosure_type", ""))

        # iTunes tags
        for field in ["summary", "explicit", "duration", "season", "episode", "episodeType"]:
            tag = f"{{{NS['itunes']}}}{field}"
            elem = ET.SubElement(new_item, tag)
            elem.text = form.get(f"itunes_{field}", "")

        # iTunes image
        tag = f"{{{NS['itunes']}}}image"
        image = ET.SubElement(new_item, tag)
        image.set("href", form.get("itunes_image", ""))

        # Insert BEFORE the first existing <item> (newest-first)
        first_item = channel.find("item")
        if first_item is not None:
            channel.insert(channel.index(first_item), new_item)
        else:
            channel.append(new_item)

        # Save RSS
        tree.write(RSS_FILE, encoding="utf-8", xml_declaration=True, pretty_print=True)
        return redirect("/")

    return render_template("add.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)