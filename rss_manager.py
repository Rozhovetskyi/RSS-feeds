#!/usr/bin/env python3
import argparse
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import formatdate

MAX_ITEMS = 7
FEEDS_DIR = "feeds"

def ensure_feeds_dir():
    if not os.path.exists(FEEDS_DIR):
        os.makedirs(FEEDS_DIR)

def get_feed_path(topic):
    # Sanitize topic to be filename safe-ish
    safe_topic = "".join(c for c in topic if c.isalnum() or c in ('-', '_')).strip()
    return os.path.join(FEEDS_DIR, f"{safe_topic}.xml")

def create_initial_feed(topic):
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    title = ET.SubElement(channel, "title")
    title.text = f"{topic} News"
    desc = ET.SubElement(channel, "description")
    desc.text = f"Latest news about {topic}"
    link = ET.SubElement(channel, "link")
    link.text = "https://github.com/jules/feeds" # Placeholder
    return ET.ElementTree(rss)

def add_item(tree, title_text, link_text, summary_text):
    root = tree.getroot()
    channel = root.find("channel")

    # Deduplication check
    current_links = {item.find("link").text for item in channel.findall("item") if item.find("link") is not None}
    if link_text in current_links:
        print(f"Duplicate found, skipping: {link_text}")
        return False

    # Create new item
    item = ET.Element("item")

    t = ET.SubElement(item, "title")
    t.text = title_text

    l = ET.SubElement(item, "link")
    l.text = link_text

    d = ET.SubElement(item, "description")
    d.text = summary_text

    p = ET.SubElement(item, "pubDate")
    p.text = formatdate(datetime.now().timestamp())

    g = ET.SubElement(item, "guid")
    g.text = link_text

    # Insert at the top of items (after channel metadata)
    # We need to find where the first 'item' is, or append if none
    items = channel.findall("item")
    if items:
        # Find the index of the first item
        first_item_index = list(channel).index(items[0])
        channel.insert(first_item_index, item)
    else:
        channel.append(item)

    # Prune
    items = channel.findall("item")
    if len(items) > MAX_ITEMS:
        # Remove the last ones
        for item_to_remove in items[MAX_ITEMS:]:
            channel.remove(item_to_remove)

    return True

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def main():
    parser = argparse.ArgumentParser(description="Manage RSS feeds for Jules.")
    parser.add_argument("--topic", required=True, help="Topic name (used for filename)")
    parser.add_argument("--title", required=True, help="Article title")
    parser.add_argument("--link", required=True, help="Article URL")
    parser.add_argument("--summary", default="", help="Article summary")

    args = parser.parse_args()

    ensure_feeds_dir()
    filepath = get_feed_path(args.topic)

    if os.path.exists(filepath):
        try:
            tree = ET.parse(filepath)
        except ET.ParseError:
            print(f"Error parsing {filepath}, creating new one.")
            tree = create_initial_feed(args.topic)
    else:
        tree = create_initial_feed(args.topic)

    if add_item(tree, args.title, args.link, args.summary):
        root = tree.getroot()
        indent(root)
        tree.write(filepath, encoding="utf-8", xml_declaration=True)
        print(f"Item added to {filepath}")
    else:
        print("No changes made.")

if __name__ == "__main__":
    main()
