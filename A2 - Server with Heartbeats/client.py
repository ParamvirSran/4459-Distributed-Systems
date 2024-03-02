import GRPC
import replication_pb2
import replication_pb2_grpc
# import heartbeat_service_pb2
# import heartbeat_service_pb2_grpc


# main function to connect toe primary server
def main():
    # connect to primary server
    channel = GRPC.insecure_channel('localhost:50051')
    stub = replication_pb2_grpc.ReplicationStub(channel)
    # create a request message
    request = replication_pb2.ReplicationRequest()
    request.message = "Hello"
    # send the request to the server
    response = stub.replicate(request)
    # print the response
    print("Replication client received: " + response.message)
    return 0


if __name__ == '__main__':
    main()
