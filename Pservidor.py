import time
from concurrent import futures

import grpc
import Pservidor_pb2
import Pservidor_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

userPort = ""
file_list = []
users = None

class PeerServiceServicer(Pservidor_pb2_grpc.PeerServiceServicer):

    def GetPortForUser(self, request, context):
        user = request.user
        print(userPort)
        if user == users:
            return Pservidor_pb2.PortResponse(port=userPort)
        else:
            return Pservidor_pb2.PortResponse(port="BadPort") 

    def SetUserPort(self, request, context):
        user = request.user
        global users
        if users == None:
            users = user
            return Pservidor_pb2.Response(success=True)
        else:
            return Pservidor_pb2.Response(success=False)
        
    def GetFile(self, request, context):
        filename = request.filename
        if filename in file_list:
            return Pservidor_pb2.FileResponse(content=filename)
        else:
            return Pservidor_pb2.FileResponse(content="File '{}' not found".format(filename))

    def CreateFile(self, request, context):
        filename = request.filename
        global file_list
        for file in filename:
            file_list.append(file)
        return Pservidor_pb2.FileCreateResponse(success=True)


def serve():
    global userPort
    for port in range(50051, 50061):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        Pservidor_pb2_grpc.add_PeerServiceServicer_to_server(PeerServiceServicer(), server)
        try:
            userPort = port
            server.add_insecure_port('[::]:{}'.format(port))
            server.start()
            print("The server is running on port {}...".format(port))
            break 
        except Exception as e:
            print("Could not start the server on port {}. Trying another port...".format(port))
            if port == 50060:
                print("Could not start the server on any available port.")
                return
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()

