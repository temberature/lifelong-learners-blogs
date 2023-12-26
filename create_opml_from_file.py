import xml.etree.ElementTree as ET
import feedparser
from xml.dom import minidom

# Function to prettify the XML
def prettify(element):
    rough_string = ET.tostring(element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

# Function to create an OPML file for Lifelong Learners
def create_opml(feed_list, output_file):
    root = ET.Element("opml", version="2.0")
    head = ET.SubElement(root, "head")
    
    # Adding metadata related to Lifelong Learners
    title = ET.SubElement(head, "title")
    title.text = "Lifelong Learners RSS Feed List"
    description = ET.SubElement(head, "description")
    description.text = "A curated list of RSS feeds for Lifelong Learners."

    body = ET.SubElement(root, "body")

    for feed_url in feed_list:
        feed = feedparser.parse(feed_url)
        feed_title = feed.feed.get('title', 'No title available')
        feed_description = feed.feed.get('description', 'No description available')
        
        # Adding each feed with enhanced information
        outline = ET.SubElement(body, "outline", text=feed_title, type="rss", xmlUrl=feed_url, description=feed_description)

    # Prettify and write the OPML to a file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(prettify(root))

# Function to read RSS feeds from a text file
def read_feeds_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

# File containing the list of RSS feeds
input_file = "RSSList.txt"

# Output file name
output_opml_file = "lifelong_learners_rss_feeds.opml"

# Read RSS feeds from file
rss_list = read_feeds_from_file(input_file)

# Creating OPML for Lifelong Learners
create_opml(rss_list, output_opml_file)

print(f"Lifelong Learners OPML file created: {output_opml_file}")
