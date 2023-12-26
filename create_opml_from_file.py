# import xml.etree.ElementTree as ET
import xml.etree.ElementTree as ET

# Function to create an OPML file from a list of RSS feeds
def create_opml(feed_list, output_file):
    # Create the root element
    root = ET.Element("opml", version="2.0")
    # Create the head element
    head = ET.SubElement(root, "head")
    # Adding a title to the head (Optional)
    title = ET.SubElement(head, "title")
    title.text = "RSS Feeds OPML"
    # Create the body element
    body = ET.SubElement(root, "body")
    # Adding each feed to the body
    for feed in feed_list:
        outline = ET.SubElement(body, "outline", type="rss", text=feed, xmlUrl=feed)
    # Create an ElementTree from the root element
    tree = ET.ElementTree(root)
    # Write the OPML to a file
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

# Function to read RSS feeds from a text file
def read_feeds_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

# File containing the list of RSS feeds
input_file = "RSSList.txt"

# Output file name
output_opml_file = "rss_feeds.opml"

# Read RSS feeds from file
rss_list = read_feeds_from_file(input_file)

# Creating OPML
create_opml(rss_list, output_opml_file)

print(f"OPML file created: {output_opml_file}")
