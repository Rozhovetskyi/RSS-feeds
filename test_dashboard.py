import unittest
from unittest.mock import patch, MagicMock
import json
import xml.etree.ElementTree as ET
import dashboard
from io import BytesIO
import http.server

class TestDashboard(unittest.TestCase):

    @patch('urllib.request.urlopen')
    def test_fetch_config(self, mock_urlopen):
        # Mock response
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({"key": "value"}).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        config = dashboard.fetch_config("http://example.com/config.json")
        self.assertEqual(config, {"key": "value"})

    @patch('urllib.request.urlopen')
    def test_fetch_rss(self, mock_urlopen):
        # Mock response
        rss_content = """
        <rss version="2.0">
            <channel>
                <title>Test Feed</title>
                <item>
                    <title>Item 1</title>
                    <link>http://example.com/item1</link>
                </item>
            </channel>
        </rss>
        """
        mock_response = MagicMock()
        mock_response.read.return_value = rss_content.encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        rss_root = dashboard.fetch_rss("http://example.com/feed.xml")
        self.assertIsNotNone(rss_root)
        channel = rss_root.find("channel")
        self.assertIsNotNone(channel)
        self.assertEqual(channel.find("title").text.strip(), "Test Feed")

    @patch('dashboard.fetch_rss')
    def test_render_dashboard(self, mock_fetch_rss):
        # Mock config
        config = {
            "activeDashboardId": "d1",
            "dashboards": [
                {
                    "id": "d1",
                    "name": "Test Dashboard",
                    "widgets": [
                        {
                            "type": "rss",
                            "title": "Widget 1",
                            "config": {"url": "http://feed.xml", "maxItems": "1"}
                        }
                    ]
                }
            ]
        }

        # Mock RSS
        rss_content = """
        <rss version="2.0">
            <channel>
                <title>Test Feed</title>
                <item>
                    <title>Item 1</title>
                    <link>http://example.com/item1</link>
                    <description>Desc 1</description>
                </item>
                <item>
                    <title>Item 2</title>
                    <link>http://example.com/item2</link>
                </item>
            </channel>
        </rss>
        """
        mock_fetch_rss.return_value = ET.fromstring(rss_content)

        html = dashboard.render_dashboard(config)
        self.assertIn("Test Dashboard", html)
        self.assertIn("Widget 1", html)
        self.assertIn("Item 1", html)
        self.assertNotIn("Item 2", html) # maxItems=1

    def test_handler(self):
        handler = dashboard.DashboardHandler.__new__(dashboard.DashboardHandler)
        handler.request = MagicMock()
        handler.client_address = ('127.0.0.1', 8888)
        handler.server = MagicMock()
        handler.wfile = BytesIO()
        handler.rfile = BytesIO()
        handler.path = '/demo'
        handler.protocol_version = "HTTP/1.0"
        handler.request_version = "HTTP/1.0"
        handler.command = "GET"
        handler.headers = {}
        # BaseHTTPRequestHandler uses sys.stderr for logging by default, or log_message
        handler.log_request = MagicMock()

        # Mock fetch_config and render_dashboard
        with patch('dashboard.fetch_config') as mock_fetch:
            with patch('dashboard.render_dashboard') as mock_render:
                mock_fetch.return_value = {}
                mock_render.return_value = "<html>Test</html>"

                handler.do_GET()

                response = handler.wfile.getvalue().decode('utf-8')
                # The response status line is written first
                # Check for 200 OK
                # Note: send_response writes "HTTP/1.0 200 OK\r\n"
                self.assertTrue(response.startswith("HTTP/1.0 200 OK"))
                self.assertIn("Content-type: text/html", response)
                self.assertIn("<html>Test</html>", response)

if __name__ == '__main__':
    unittest.main()
