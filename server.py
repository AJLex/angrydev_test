import socket


from part_1 import get_data_from_file,  get_dict_trie_like, suggest_options


# Function configures the server
def setup_server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # connection is TCP/IPv4
    host = ''
    server_adress = (host, port)
    sock.bind(server_adress)
    sock.listen(1)  # client queue length
    return sock


# Function prepares server for client request processing
def preparing_server(path_to_file, sock):
    dict_trie = get_dict_trie_like(get_data_from_file(path_to_file))  # prepare dictionary
    conn, addr = sock.accept()  # waiting for client connection
    data = conn.recv(1024).decode('utf-8')  # getting message from client, when he connected
    print(data, 'from ', addr[0])
    return dict_trie, conn


# Function processing client request
def client_request_processing(dict_trie, conn, max_len):
    while True:
        data = conn.recv(1024).decode('utf-8')
        if data == 'exit':  # if client sends "exit", server turns off
            break
        try:
            command, prefix = data.split()
            if command == 'get':
                prefix = prefix[1: len(prefix) - 1]
                prefix_options = suggest_options(dict_trie, [prefix], max_len)
                for word_info in prefix_options[0][1]:
                    conn.send(bytes(word_info[0] + 'end', encoding='utf-8'))  # "end" says to client that all data was obtained
                    conn.recv(1024).decode('utf-8')  # server gets answer from client, when client gets all data
        except:
            conn.send(bytes('Invalid command' + 'end', encoding='utf-8'))
        conn.send(bytes('\n', encoding='utf-8'))  # server sending "\n", when request processing is ending


if __name__ == "__main__":
    path_to_file = input("Enter path to dictionary:\n> ")
    sock = setup_server(int(input("Enter port:\n> ")))
    dict_trie, conn = preparing_server(path_to_file, sock)
    client_request_processing(dict_trie, conn, max_len=10)
    conn.close()