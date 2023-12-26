import feedparser
import requests
from requests.exceptions import RequestException

# Function to check if the URL potentially contains a valid feed
def is_valid_feed(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        content = response.content
        try:
            # Try to parse with UTF-8 encoding
            feed = feedparser.parse(content)
        except UnicodeDecodeError:
            # Try to parse with a different encoding if UTF-8 fails
            content = content.decode('iso-8859-1').encode('utf-8')
            feed = feedparser.parse(content)
        
        if feed.bozo == 0:
            return True
        else:
            return False
    except RequestException as e:
        print(f"Error accessing URL {url}: {e}")
        return False
    except Exception as e:
        print(f"Other error when processing URL {url}: {e}")
        return False

# ... Rest of the script remains the same ...

# Function to extract feed information
def extract_feed_info(feed_url):
    if not is_valid_feed(feed_url):
        return feed_url, "Invalid or Inaccessible URL", "This URL did not return a valid feed."

    feed = feedparser.parse(feed_url)
    title = feed.feed.get('title', 'No title available')
    description = feed.feed.get('description', 'No description available')
    link = feed.feed.get('link', feed_url)  # Use feed URL as fallback
    return link, title, description

# Function to generate README from a template and RSS feed data
def generate_readme_from_template(template_path, rss_list_path, output_path):
    with open(template_path, 'r') as file:
        template_content = file.read()

    # Placeholder for RSS feeds in the template
    placeholder_start = "<!-- RSS_FEEDS_START -->"
    placeholder_end = "<!-- RSS_FEEDS_END -->"
    start_index = template_content.find(placeholder_start) + len(placeholder_start)
    end_index = template_content.find(placeholder_end)

    rss_feeds_content = ""
    with open(rss_list_path, 'r') as file:
        for line in file:
            feed_url = line.strip()
            if feed_url:
                link, title, description = extract_feed_info(feed_url)
                rss_feeds_content += f"### [{title}]({link})\n**Description:** {description}\n\n"

    # Combine template with RSS feeds content
    final_content = (template_content[:start_index] +
                     "\n" + rss_feeds_content +
                     template_content[end_index:])

    # Write the final README content
    with open(output_path, 'w') as file:
        file.write(final_content)

# Paths for the templates, RSS list, and output files
template_file_en = "README_template.md"
template_file_cn = "README_template_CN.md"
rss_list_file = "RSSList.txt"
output_readme_file_en = "README.md"
output_readme_file_cn = "README_CN.md"

# Generate README.md and README_CN.md using the templates and RSS list
generate_readme_from_template(template_file_en, rss_list_file, output_readme_file_en)
generate_readme_from_template(template_file_cn, rss_list_file, output_readme_file_cn)

print(f"English and Chinese README documents created.")