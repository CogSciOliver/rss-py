# RSS Editor Web App

A simple Python web application to view, edit, and add RSS feed items through a user-friendly web interface. It displays all tags in a two-column layout, allowing you to edit existing content, add missing fields, and create new <item> entries at the top of your RSS feed.

## Features

Display all <item> entries in your rss.xml with tags and content.

Two-column form:

Left: current tag content.

Right: editable form input.

Add missing tags or input new data.

Create a new RSS <item> at the top of the feed.

Editable title, description, link, guid, pubDate, and other tags.

Automatically saves changes back to rss.xml.

## Requirements

Python 3.7+

Flask

Install Flask using pip:

```
pip install flask
```

## Usage

Place your rss.xml in the same folder as rss_editor.py.

Run the application:

```
python3 rss_editor.py
```

Open your browser and go to:

```
http://127.0.0.1:5000
```

You can now:

- Edit existing items.
- Add missing fields.
- Add a new RSS item at the top.

Changes are automatically saved back to rss.xml.

## Notes

Development server only: Do not use this in production; use a WSGI server for production deployment.

On macOS, if you see a 403 Forbidden, ensure the app is running with host="0.0.0.0" and access via http://localhost:5000.

Supports editing longer fields (like <description>) with textareas.

## Example

Existing item view:

Current Content | Editable Input
Title: "Episode 1" | [textarea with editable title]
Description: "Learn about Marsupials" | [textarea for editing]

Add new item: A form at the top allows inputting title, description, link, GUID, and pubDate.

## License

MIT License – free to use, modify, and distribute.

## Podcast Need to Knows 
Apple Podcasts (formerly iTunes) defines three main episode types to categorize content, which are used for organization and display in the app: Full, Trailer, and Bonus. These types affect how episodes are ordered, whether they show a number, and how they are presented to listeners. 

### Full (Default): 
The standard, full-length content for a podcast episode, usually accompanied by an episode number.
### Trailer (Teaser): 
A short, promotional snippet designed to introduce a new show or season, typically displayed at the beginning and lacking an episode number.
### Bonus (Extra Content): 
Bonus material such as behind-the-scenes, interviews, or special updates. These are not numbered and can be ordered by publication date.