import socket
import argparse
import os
import logging
import mimetypes

def get_mime_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or "application/octet-stream"

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler("server.log"),  # Лог в файл
        logging.StreamHandler()  # Лог в консоль
    ]
)
logger = logging.getLogger()

def parse():
    parser = argparse.ArgumentParser(description="HTTP 1.1 Server")
    parser.add_argument('-p', '--port', type=int, default=8080, help="Port to run the server on")
    parser.add_argument('-d', '--directory', type=str, default=os.getcwd(), help="Directory to serve files from")
    parser.add_argument('-H', '--headers', nargs='+', help="Default headers to include in responses")
    
    return parser.parse_args()

def handle_request(client_socket, directory, default_headers):
    try:
        request = client_socket.recv(1024).decode('utf-8')
        if not request:
            client_socket.sendall("HTTP/1.1 400 Bad Request\r\n\r\nBad Request".encode('utf-8'))
            return
        
        lines = request.split("\r\n")
        if len(lines) < 1 or len(lines[0].split()) < 3:
            client_socket.sendall("HTTP/1.1 400 Bad Request\r\n\r\nBad Request".encode('utf-8'))
            return

        logger.info(f"Received request: {lines[0]}")

        # метод, путь и версия HTTP
        method, path, _ = lines[0].split()
        logger.info(f"Method: {method}, Path: {path}")  

        if method == "GET":
            file_path = os.path.join(directory, path.strip('/'))

            if os.path.isfile(file_path):
                mime_type = get_mime_type(file_path)
                with open(file_path, 'rb') as f:
                    file_data = f.read()

                response = f"HTTP/1.1 200 OK\r\n"
                response += f"Content-Type: {mime_type}\r\n"  
                response += f"Content-Length: {len(file_data)}\r\n"  
                for header in default_headers:
                    response += f"{header}\r\n"
                response += "\r\n"  

                client_socket.sendall(response.encode('utf-8'))
                client_socket.sendall(file_data)
                
                logger.info(f"Sent response: 200 OK, {len(file_data)} bytes sent")  

            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\nFile not found"
                client_socket.sendall(response.encode('utf-8'))
                logger.warning(f"File not found: {file_path}") 

        elif method == "POST":
            headers, body = request.split("\r\n\r\n", 1) 
            logger.info(f"POST Data: {body}")  

            file_name = path.strip('/')  
            if not file_name:  
                file_name = "post_data.txt"
            file_path = os.path.join(directory, file_name)

            with open(file_path, 'wb') as file:
                file.write(body.encode('utf-8')) 


            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type: text/plain\r\n"
            response += f"Content-Length: {len(body)}\r\n"
            for header in default_headers:
                response += f"{header}\r\n"
            response += "\r\n"
            response += f"Data saved to {file_path}"
            
            client_socket.sendall(response.encode('utf-8'))
            logger.info(f"Data saved to file: {file_path}, {len(body)} bytes received.") 

        elif method == "OPTIONS":
            response = "HTTP/1.1 204 No Content\r\nAllow: GET, POST, OPTIONS\r\n"
            for header in default_headers:
                response += f"{header}\r\n"
            response += "\r\n"
            client_socket.sendall(response.encode('utf-8'))
            logger.info(f"Sent OPTIONS response: 204 No Content")  

        else:
            response = "HTTP/1.1 405 Method Not Allowed\r\n\r\nMethod not allowed"
            client_socket.sendall(response.encode('utf-8'))
            logger.warning(f"Method not allowed: {method}")  

    except Exception as e:
        logger.error(f"Error handling request: {e}")  
        client_socket.sendall("HTTP/1.1 500 Internal Server Error\r\n\r\nInternal Server Error".encode('utf-8'))


def run_server(port, directory, default_headers):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    logger.info(f"Serving HTTP on port {port} from directory {directory}")
    
    while True:
        client_socket, _ = server_socket.accept()
        handle_request(client_socket, directory, default_headers)
        client_socket.close()

if __name__ == "__main__":
    args = parse()
    headers = args.headers or ["Access-Control-Allow-Origin: *", "Access-Control-Allow-Methods: GET, POST, OPTIONS"]
    run_server(args.port, args.directory, headers)
