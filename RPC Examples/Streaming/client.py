import grpc
import streaming_pb2
import streaming_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = streaming_pb2_grpc.ServerToClientStreamingExampleStub(channel)
        response_iterator = stub.StreamMessages(streaming_pb2.Empty())

        for response in response_iterator:
            print(f"Received: {response.content}")

if __name__ == '__main__':
    run()

