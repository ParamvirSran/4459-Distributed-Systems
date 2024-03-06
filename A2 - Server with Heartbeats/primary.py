# Paramvir Sran, 251102997

import datetime
import time
from concurrent import futures

import grpc

import heartbeat_service_pb2
import heartbeat_service_pb2_grpc
import replication_pb2
import replication_pb2_grpc


# Defines the gRPC service for the primary server.
class PrimarySequenceServicer(replication_pb2_grpc.SequenceServicer):
    def __init__(self):
        # Initializes an empty dictionary to store key-value pairs.
        self.data = {}
        # Establishes a gRPC channel to the backup server for replication.
        self.backup_channel = grpc.insecure_channel("localhost:50052")
        self.backup_stub = replication_pb2_grpc.SequenceStub(self.backup_channel)

    def Write(self, request, context):
        # Validates the incoming request to ensure it contains both key and value.
        if not request.key or not request.value:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Key and value cannot be empty.")
            return replication_pb2.WriteResponse(
                ack="Invalid request: Empty key or value."
            )

        try:
            # Attempts to replicate the write operation to the backup server.
            self.backup_stub.Write(request)
            # Upon successful replication, the write operation is applied locally.
            self.data[request.key] = request.value

            # Logs the operation with a timestamp.
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("primary.txt", "a") as log_file:
                log_file.write(
                    f"{current_time} - Key: {request.key}, Value: {request.value}\n"
                )

            return replication_pb2.WriteResponse(
                ack=f"Write operation successful for {request.key}"
            )
        except grpc.RpcError as e:
            # Handles any communication errors with the backup server.
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            context.set_details("Backup server is unavailable.")
            return replication_pb2.WriteResponse(
                ack="Backup server communication failed."
            )

    def send_heartbeat(self):
        # Sends heartbeat messages to the ViewService to indicate aliveness.
        with grpc.insecure_channel("localhost:50053") as channel:
            stub = heartbeat_service_pb2_grpc.ViewServiceStub(channel)
            while True:
                try:
                    stub.Heartbeat(
                        heartbeat_service_pb2.HeartbeatRequest(
                            service_identifier="primary"
                        )
                    )
                    print(
                        f"Heartbeat sent for primary at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    )
                except grpc.RpcError as e:
                    print(f"Failed to send heartbeat: {str(e)}")
                time.sleep(5)  # Sends a heartbeat every 5 seconds.


# Starts and runs the primary server.
def serve():
    primary_servicer = PrimarySequenceServicer()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    replication_pb2_grpc.add_SequenceServicer_to_server(primary_servicer, server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Primary server running on port 50051.")
    futures.ThreadPoolExecutor(max_workers=1).submit(primary_servicer.send_heartbeat)

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Primary server shutting down.")
    finally:
        server.stop(None)  # Ensures a graceful shutdown.


if __name__ == "__main__":
    serve()
