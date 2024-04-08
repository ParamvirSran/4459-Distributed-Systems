import grpc
import helloworld_pb2
import helloworld_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
      stub = helloworld_pb2_grpc.GreeterStub(channel)
      response = stub.SayHello(helloworld_pb2.HelloRequest(name='Hanan'))
      print("Greeter client received following from server: " + response.message)   
run()


