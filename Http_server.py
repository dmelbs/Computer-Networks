import os
import socket

def server(port):
    host = "0.0.0.0" # ourselves
    root = "/path/to/root/directory" # the root directory that contains the files the server can access
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()
    
    while True:
        conn, addr = sock.accept()
        data = ""
        while True:
            chunk = conn.recv(1024)
            if not chunk:
                break
            data += chunk.decode('utf-8', 'ignore')
            
        # parse the request
        request_lines = data.split("\r\n")
        method, path, protocol = request_lines[0].split()
        
        # check if the requested file is under the root directory
        full_path = os.path.abspath(os.path.join(root, path.lstrip("/")))
        if not full_path.startswith(root):
            response_headers = "HTTP/1.1 403 Forbidden\r\n\r\n"
            response_data = "403 Forbidden: Access denied"
        elif not os.path.isfile(full_path):
            response_headers = "HTTP/1.1 404 Not Found\r\n\r\n"
            response_data = "404 Not Found: " + path
        else:
            with open(full_path, "r") as f:
                file_data = f.read()
                
            response_headers = "HTTP/1.1 200 OK\r\nContent-Length: " + str(len(file_data)) + "\r\n\r\n"
            response_data = file_data
            
        # send the response
        conn.sendall(response_headers.encode())
        conn.sendall(response_data.encode())
        conn.close()
