from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
import re

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        
        url = data.get('url')
        if not url:
            self.send_error(400, 'URL is required')
            return
            
        video_id = self.get_video_id(url)
        if not video_id:
            self.send_error(400, 'Invalid YouTube URL')
            return
            
        transcript = self.get_transcript(video_id)
        if not transcript:
            self.send_error(400, 'Could not retrieve transcript')
            return
            
        summary = self.summarize_text(transcript)
        if not summary:
            self.send_error(500, 'Could not generate summary')
            return
            
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'summary': summary}).encode())

    def get_video_id(self, url):
        match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url)
        return match.group(1) if match else None

    def get_transcript(self, video_id):
        try:
            from urllib.request import urlopen
            url = f'https://www.youtube.com/watch?v={video_id}'
            response = urlopen(url)
            html = response.read().decode('utf-8')
            
            # Basic transcript extraction (this is a simplified version)
            # Note: This won't work for all videos as YouTube's transcript system is complex
            # For a real implementation, you'd need to use the YouTube Data API
            transcript = re.findall(r'"simpleText":"([^"]+)"', html)
            return ' '.join(transcript)
        except Exception as e:
            print(f"Error getting transcript: {e}")
            return None

    def summarize_text(self, text):
        # Basic summarizer using first 200 characters
        return text[:200] + '...' if len(text) > 200 else text

def run(server_class=HTTPServer, handler_class=RequestHandler, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
