import socket 
import tqdm
import os 

SEPARATOR="<SEPARATOR>"
BUFFER_SIZE=1024 #send 1024 bytes each time 

host_name = socket.gethostname()
ip = socket.gethostbyname(host_name)
port=5001 

file_name="/media/kali/4bc6570e-3d60-46c1-aa75-1bdbe9ddee20/kalilinux/python/fileSharing/folder/file.mp4"
file_size=os.path.getsize(file_name)


#lets create TCP socket

tcp_protocol=socket.socket()

print(f"[+] connecting to {ip}:{port}")

tcp_protocol.connect((ip,port))

print("[+] connected.")


tcp_protocol.send(f"{file_name}{SEPARATOR}{file_size}".encode())

#start sending file

progress=tqdm.tqdm(range(file_size),f"Sending {file_name}",unit="B", unit_scale=True,unit_divisor=1024)
with open(file_name,'rb') as f:

    for _ in progress:
        #read the bytes from the file

        bytes_read=f.read(BUFFER_SIZE)
        if not bytes_read:
            break 
        
        # we use send all to assure transmission in busy network

        tcp_protocol.sendall(bytes_read)            

        #update the progress

        progress.update(len(bytes_read))


tcp_protocol.close()

