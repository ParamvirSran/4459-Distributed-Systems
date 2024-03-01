# Paramvir Sran, 251102997
# client implementation to call the inventory service methods from the server using gRPC

import grpc
import inventory_pb2
import inventory_pb2_grpc
from google.protobuf import empty_pb2


# The run function is used to call the service methods
def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = inventory_pb2_grpc.InventoryServiceStub(channel)

        while True:
            responses = stub.GetAllProducts(empty_pb2.Empty())

            for response in responses:
                print('Received product:', response)


if __name__ == '__main__':
    run()
