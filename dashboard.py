import http.server
import socketserver
import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
import sys
import html
import re
import time
import threading

# Constants
PORT = 8080
CONFIG_URL = "https://ar-xr.com/dashboard-demo/demo-config.json"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
CACHE_TTL = 300 # 5 minutes

# Simple in-memory cache: url -> (content, timestamp)
CACHE = {}
CACHE_LOCK = threading.Lock()

def validate_url(url):
    """Validates that the URL uses http or https scheme."""
    if not url:
        return False
    try:
        parsed = urllib.parse.urlparse(url)
        return parsed.scheme in ('http', 'https')
    except Exception:
        return False

def fetch_content(url):
    """Fetches content from a URL with custom headers and caching."""
    if not validate_url(url):
        print(f"Invalid URL scheme: {url}", file=sys.stderr)
        return None

    with CACHE_LOCK:
        if url in CACHE:
            content, timestamp = CACHE[url]
            if time.time() - timestamp < CACHE_TTL:
                return content
            else:
                del CACHE[url]

    try:
        req = urllib.request.Request(
            url,
            data=None,
            headers={'User-Agent': USER_AGENT}
        )
        # Using default SSL context for security
        with urllib.request.urlopen(req) as response:
            content = response.read()
            with CACHE_LOCK:
                CACHE[url] = (content, time.time())
            return content
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None

def fetch_config(url):
    """Fetches and parses the JSON configuration from the given URL."""
    content = fetch_content(url)
    if content:
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from {url}: {e}", file=sys.stderr)
            return None
    return None

def fetch_rss(url):
    """Fetches and parses an RSS feed from the given URL."""
    content = fetch_content(url)
    if content:
        try:
            return ET.fromstring(content)
        except ET.ParseError as e:
            print(f"Error parsing XML from {url}: {e}", file=sys.stderr)
            return None
    return None

def clean_html(raw_html):
    """Removes HTML tags and escapes the result."""
    if not raw_html:
        return ""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return html.escape(cleantext)

def render_dashboard(config):
    """Renders the dashboard HTML based on the configuration."""
    if not config:
        return "<html><body><h1>Error loading configuration</h1></body></html>"

    active_dashboard_id = config.get("activeDashboardId")
    dashboards = config.get("dashboards", [])

    active_dashboard = next((d for d in dashboards if d["id"] == active_dashboard_id), None)

    if not active_dashboard:
        return "<html><body><h1>Active dashboard not found</h1></body></html>"

    dashboard_name = html.escape(active_dashboard.get('name', 'Dashboard'))

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{dashboard_name}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .dashboard {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }}
            .widget {{ border: 1px solid #ccc; padding: 15px; border-radius: 5px; }}
            .widget h2 {{ margin-top: 0; font-size: 1.2em; }}
            .feed-item {{ margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 5px; }}
            .feed-item:last-child {{ border-bottom: none; }}
            .feed-item a {{ text-decoration: none; color: #007bff; }}
            .feed-item a:hover {{ text-decoration: underline; }}
            .feed-date {{ font-size: 0.8em; color: #666; }}
            .feed-desc {{ font-size: 0.9em; margin-top: 5px; }}
        </style>
    </head>
    <body>
        <h1>{dashboard_name}</h1>
        <div class="dashboard">
    """

    widgets = active_dashboard.get("widgets", [])
    for widget in widgets:
        if widget.get("type") == "rss":
            widget_config = widget.get("config", {})
            rss_url = widget_config.get("url")
            show_desc = widget_config.get("showDescription", False)
            show_date = widget_config.get("showDate", False)
            max_items = widget_config.get("maxItems")
            widget_title = html.escape(widget.get("title", "RSS Feed"))

            html_content += f'<div class="widget"><h2>{widget_title}</h2>'

            if rss_url:
                rss_root = fetch_rss(rss_url)
                if rss_root is not None:
                    channel = rss_root.find("channel")
                    if channel is not None:
                        items = channel.findall("item")
                        if max_items:
                            try:
                                items = items[:int(max_items)]
                            except ValueError:
                                pass # Ignore if maxItems is not an integer

                        for item in items:
                            title_elem = item.find("title")
                            title = title_elem.text if title_elem is not None and title_elem.text else "No Title"

                            link_elem = item.find("link")
                            link = link_elem.text if link_elem is not None and link_elem.text else "#"

                            if not validate_url(link):
                                link = "#"

                            desc_elem = item.find("description")
                            desc = desc_elem.text if desc_elem is not None and desc_elem.text else ""

                            pub_date_elem = item.find("pubDate")
                            pub_date = pub_date_elem.text if pub_date_elem is not None and pub_date_elem.text else ""

                            safe_title = html.escape(title)
                            safe_link = html.escape(link)
                            safe_date = html.escape(pub_date)
                            safe_desc = clean_html(desc)

                            html_content += '<div class="feed-item">'
                            html_content += f'<a href="{safe_link}" target="_blank">{safe_title}</a>'
                            if show_date and pub_date:
                                html_content += f'<div class="feed-date">{safe_date}</div>'
                            if show_desc and desc:
                                html_content += f'<div class="feed-desc">{safe_desc[:200]}...</div>'
                            html_content += '</div>'
                    else:
                        html_content += "<p>Invalid RSS feed format.</p>"
                else:
                    html_content += "<p>Failed to load feed.</p>"
            else:
                html_content += "<p>No RSS URL configured.</p>"

            html_content += '</div>'

    html_content += """
        </div>
    </body>
    </html>
    """
    return html_content

class DashboardHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/demo':
            config = fetch_config(CONFIG_URL)
            if config:
                html_content = render_dashboard(config)
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))
            else:
                 self.send_error(500, "Failed to load configuration")
        else:
            self.send_error(404, "Not Found")

def run_server(port=PORT):
    # Use ThreadingTCPServer for better concurrency
    with socketserver.ThreadingTCPServer(("", port), DashboardHandler) as httpd:
        print(f"Serving at port {port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            httpd.server_close()
            print("Server stopped.")

if __name__ == "__main__":
    run_server()
