import time
from concurrent import futures

import grpc
import Pservidor_pb2
import Pservidor_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class PeerServiceServicer(Pservidor_pb2_grpc.PeerServiceServicer):

    def GetFile(self, request, context):
        filename = request.filename
        return Pservidor_pb2.FileResponse(content="Content of the file '{}'\n".format(filename))

    def CreateFile(self, request, context):
        filename = request.filename
        content = request.content
        return Pservidor_pb2.FileCreateResponse(success=True)

def serve():
    for port in range(50051, 50061):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        Pservidor_pb2_grpc.add_PeerServiceServicer_to_server(PeerServiceServicer(), server)
        try:
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
