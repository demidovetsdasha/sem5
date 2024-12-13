import socket
import argparse
from urllib.parse import urlparse

def parse_args():
    parser = argparse.ArgumentParser(description="HTTP 1.1 Client")
    parser.add_argument('-u', '--url', type=str, required=True, help="URL to send the request to")
    parser.add_argument('-m', '--method', type=str, default="GET", help="HTTP method to use")
    parser.add_argument('-d', '--data', type=str, help="Request body")
    parser.add_argument('--headers', nargs='+', help="Custom headers")
    parser.add_argument('--template', type=str, help="Path to file with request template")  
    return parser.parse_args()

def create_request(url, method, headers, data):
    parsed_url = urlparse(url)  

    host = parsed_url.hostname
    port = parsed_url.port if parsed_url.port else 80  
    path = parsed_url.path if parsed_url.path else '/'  

    print(f"Parsed URL: {parsed_url}")
    print(f"Host: {host}, Port: {port}, Path: {path}")

    if host is None:
        raise ValueError("Host not found in the URL. Please check your URL format.")
    
    request = f"{method} {path} HTTP/1.1\r\nHost: {host}\r\n"
    if headers:
        for header in headers:
            request += f"{header}\r\n"
    if data:
        request += f"Content-Length: {len(data)}\r\n\r\n{data}"
    else:
        request += "\r\n"
    return request, host, port

def handle_response(response, is_binary=False):
    if is_binary:
        print(f"Received binary data ({len(response)} bytes)")
    else:
        if "200 OK" in response:
            print("Request was successful")
        elif "404 Not Found" in response:
            print("Error: File not found")
        elif "405 Method Not Allowed" in response:
            print("Error: Method not allowed")
        elif "201 Created" in response:
            print("File created successfully")
        elif "204 No Content" in response:
            print("No content (OPTIONS request)")
        else:
            print(f"Unexpected response: {response}")

def send_request(url, method, headers, data):
    request, host, port = create_request(url, method, headers, data)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))  
        client_socket.sendall(request.encode('utf-8'))
        
        response = b""
        while True:
            part = client_socket.recv(4096)
            if not part:
                break
            response += part
        
        try:
            response_text = response.decode('utf-8')
            handle_response(response_text, is_binary=False)
        except UnicodeDecodeError:
            handle_response(response, is_binary=True)

def load_template(template_path):
    with open(template_path, 'r') as file:
        return file.read()

if __name__ == "__main__":
    args = parse_args()

    if args.template:
        data = load_template(args.template)
    else:
        data = args.data

    send_request(args.url, args.method, args.headers, data)
