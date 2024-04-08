import grpc
from concurrent import futures
import time
import streaming_pb2
import streaming_pb2_grpc

class ServerToClientStreamingExampleServicer(streaming_pb2_grpc.ServerToClientStreamingExampleServicer):
    def StreamMessages(self, request, context):
        messages = ["Hello", "Client", "from", "Server"]

        for message in messages:
            time.sleep(1)  # Simulate some processing time
            yield streaming_pb2.Message(content=message)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    streaming_pb2_grpc.add_ServerToClientStreamingExampleServicer_to_server(
        ServerToClientStreamingExampleServicer(), server)
    server.add_insecure_port('[::]:50051')
    return server

def main():
    server = serve()
    server.start()
    try:
        while True:
            time.sleep(60 * 60 * 24)  # One day
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    main()

