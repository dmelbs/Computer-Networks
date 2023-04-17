import socket
import sys

def connect(host, port, url):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # SOCK_STREAM is a TCP connection over AF_INET, which is IP: TCP/IP
    conn.connect((host, port))
    connstr = "GET " + url + " HTTP/1.1\r\n"
    conn.send(connstr.encode())
    hoststr = "Host: " + host + "\r\n"
    conn.send(hoststr.encode())
    conn.send("\r\n".encode()) # blank line
    
    return conn # so we can read the response later

def read_response(conn):
    data = ""
    while True:
        chunk = conn.recv(1024)
        if not chunk: 
            break
        data += chunk.decode('utf-8', 'ignore')
        if '\r\n\r\n' in data:
            break
        
    return data

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide valid web server as argument")
    host = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 80
    url = "/index.html"
    
    conn = connect(host, port, url)
    response = read_response(conn)
    
    lines = response.split("\r\n")
    status_line = lines[0]
    headers = {}
    body = ""
    
    for line in lines[1:]:
        if not line.strip():
            break
        key, value = line.split(":", 1)
        headers[key.strip()] = value.strip()
        
    body = "\r\n".join(lines[lines.index("")+1:])
    
    print(status_line)
    for key, value in headers.items():
        print(f"{key}: {value}")
    print("")
    print(body)
    
    conn.close()