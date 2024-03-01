import random

import grpc
import Pservidor_pb2
import Pservidor_pb2_grpc
import requests

GRPC_SERVER_ADDRESS = 'localhost:50051'

files = []

def generate_string():
    random_number = random.randint(1, 30)
    result = "archivo" + str(random_number)
    return result

def grpc_get_file(filename):
    channel = grpc.insecure_channel(GRPC_SERVER_ADDRESS)
    client = Pservidor_pb2_grpc.PeerServiceStub(channel)
    response = client.GetFile(Pservidor_pb2.FileRequest(filename=filename))
    return response.content

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
    data = {'user': user, 'files': files}
    response = requests.post(url, json=data)
    return response.json()

def rest_search(filename):
    url = 'http://localhost:5000/search'
    params = {'filename': filename}
    response = requests.get(url, params=params)
    return response.json()

def main():
    files = [generate_string() for i in range(1, random.randint(1, 5))]
    while True:
        print("\nOptions:")
        print("1. Get file from gRPC server")
        print("2. Login to REST API server")
        print("3. Logout from REST API server")
        print("4. Index files in REST API server")
        print("5. Search file in REST API server")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            filename = input("Enter filename: ")
            grpc_response = grpc_get_file(filename)
            print("gRPC server response:", grpc_response)

        elif choice == '2':
            user = input("Enter username: ")
            password = input("Enter password: ")
            ip = input("Enter IP address: ")
            login_response = rest_login(user, password, ip)
            print("REST API login response:", login_response)

        elif choice == '3':
            user = input("Enter username: ")
            logout_response = rest_logout(user)
            print("REST API logout response:", logout_response)

        elif choice == '4':
            user = input("Enter username: ")
            index_response = rest_index(user, files)
            print("REST API index response:", index_response)

        elif choice == '5':
            filename = input("Enter filename: ")
            search_response = rest_search(filename)
            print("REST API search response:", search_response)

        elif choice == '6':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == '__main__':
    main()
