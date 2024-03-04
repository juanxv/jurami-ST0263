import random

import grpc
import Pservidor_pb2
import Pservidor_pb2_grpc
import requests

GRPC_SERVER_ADDRESS_local = 'localhost:' + '50051'

files = []
search_file = ""
search_port = ""

def generate_string():
    random_number = random.randint(1, 30)
    result = "archivo" + str(random_number)
    return result

def grpc_get_file(filename, port):
    channel = grpc.insecure_channel(port)
    client = Pservidor_pb2_grpc.PeerServiceStub(channel)
    response = client.GetFile(Pservidor_pb2.FileRequest(filename=filename))
    return response.content

def grpc_create_file(files):
    channel = grpc.insecure_channel(GRPC_SERVER_ADDRESS_local)
    client = Pservidor_pb2_grpc.PeerServiceStub(channel)
    response = client.CreateFile(Pservidor_pb2.FileCreateRequest(filename=files))
    return response.success

def grpc_set_user_port(user):
    channel = grpc.insecure_channel(GRPC_SERVER_ADDRESS_local)
    client = Pservidor_pb2_grpc.PeerServiceStub(channel)
    response = client.SetUserPort(Pservidor_pb2.UserPortRequest(user=user))
    return response.success


def grpc_get_port_for_user(user):
    channel = grpc.insecure_channel(GRPC_SERVER_ADDRESS_local)
    client = Pservidor_pb2_grpc.PeerServiceStub(channel)
    response = client.GetPortForUser(Pservidor_pb2.PortForUserRequest(user=user))
    return response.port


def rest_login(user, password, ip):
    url = 'http://localhost:5000/login'
    data = {'user': user, 'password': password, 'ip': ip}
    response = requests.post(url, json=data)
    return response.json()

def rest_logout(user):
    url = 'http://localhost:5000/logout'
    data = {'user': user}
    response = requests.post(url, json=data)
    return response.json()

def rest_index(user, files):
    url = 'http://localhost:5000/index'
    data = {'user': user, 'files': files, 'port': GRPC_SERVER_ADDRESS_local}
    response = requests.post(url, json=data)
    return response.json()

def rest_search(filename):
    url = 'http://localhost:5000/search'
    params = {'filename': filename}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else: 
        return False

def main():
    global GRPC_SERVER_ADDRESS_local
    global search_file
    files = [generate_string() for _ in range(1, random.randint(2, 5))]
    logged = False 
    user = ""
    while True:
        print("\nOptions:")
        if not logged:
            print("2. Login to REST API server")
            print("6. Exit")
        else:
            print("1. Get file from gRPC server")
            print("3. Logout from REST API server")
            print("4. Index files in REST API server")
            print("5. Search file in REST API server")
            print("6. Exit")

        choice = input("Enter your choice: ")

        if not logged:
            if choice == '2':
                user = input("Enter username: ")
                password = input("Enter password: ")
                ip = input("Enter IP address: ")
                login_response = rest_login(user, password, ip)
                if login_response.get('message') == 'Login successful':
                    logged = True
                    for port in range(50051, 50061):
                        if not grpc_set_user_port(user):
                            GRPC_SERVER_ADDRESS_local = f'localhost:{port}'
                        else:
                            grpc_create_file(files)
                            break
                print("REST API login response:", login_response)
            elif choice == '6':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please enter a number between 2 and 6.")
        else:
            if choice == '1':
                filename = input("Enter filename: ")
                pserver_port = "localhost:" + input("Enter the port to get the files from: ")
                grpc_response = grpc_get_file(filename, pserver_port)
                print("gRPC server response:", grpc_response)
            elif choice == '3':
                logout_response = rest_logout(user)
                if logout_response.get('message') == 'Logout successful':
                    grpc_set_user_port("logout")
                    logged = False
                print("REST API logout response:", logout_response)
            elif choice == '4':
                index_response = rest_index(user, files)
                print("REST API index response:", index_response)
            elif choice == '5':
                filename = input("Enter filename: ")
                search_response = rest_search(filename)
                if search_response:
                    search_file = search_response['filename']
                breakpoint()
                print("REST API search response:", search_response)
            elif choice == '6':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == '__main__':
    main()
