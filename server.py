import socket 
import tqdm
import os 


server_host_name=socket.gethostname()
server_ip=socket.gethostbyname(server_host_name)
server_port=5001
BUFFER_SIZE=1024
SEPARATOR="<SEPARATOR>"

s=socket.socket()
s.bind((server_ip,server_port))
s.listen(5)
print(f"[*] Listening as {server_ip}:{server_port}")


client_socket,address=s.accept()
# if below code is executed, that means the sender is connected
print(f"[+] {address} is connected.")

# receive the file infos
# receive using client socket, not server socket

received=client_socket.recv(BUFFER_SIZE).decode()
filename,filesize=received.split(SEPARATOR)


filename=os.path.basename(filename)

#covert to integer

filesize=int(filesize)

# start receiving the file from the socket
# and writing to the file stream
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    for _ in progress:
        # read 1024 bytes from the socket (receive)
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:    
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))

# close the client socket
client_socket.close()
# close the server socket
s.close()