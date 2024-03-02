import grpc
import replication_pb2
import replication_pb2_grpc
import heartbeat_service_pb2
import heartbeat_service_pb2_grpc


# main function to connect to primary server
def main():
    # connect to primary server
    channel = grpc.insecure_channel('localhost:50051')

    # create a stub (client)
    stub = replication_pb2_grpc.SequenceStub(channel)

    # create a request
    request = replication_pb2.ReplicationRequest(message="Hello, Primary!")

    # send the request
    response = stub.replicate(request)

    # print the response
    print(response.message)

    return 0


if __name__ == '__main__':
    main()
