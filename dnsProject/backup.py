# Paramvir Sran, 251102997

import datetime
import time
from concurrent import futures

import grpc

import heartbeat_service_pb2
import heartbeat_service_pb2_grpc

# Import necessary gRPC and protobuf modules for replication and heartbeat functionality
import replication_pb2
import replication_pb2_grpc


class BackupSequenceServicer(replication_pb2_grpc.SequenceServicer):
    """
    Implements the SequenceServicer interface from replication_pb2_grpc module,
    handling write requests and managing a local store of key-value pairs.
    """

    def __init__(self):
        self.data = {}  # Initialize an empty dictionary to store key-value pairs.

    def Write(self, request, context):
        """
        Receives a write request containing a key and value, validates input,
        performs the write operation by storing the key-value pair, and logs the operation.
        """
        # Validate that both key and value are provided in the request.
        if not request.key or not request.value:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Key and value cannot be empty.")
            return replication_pb2.WriteResponse(
                ack="Invalid request: Empty key or value."
            )

        # Store the key-value pair in the data dictionary.
        self.data[request.key] = request.value

        # Log the write operation with a timestamp for auditability.
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("backup.txt", "a") as log_file:
            log_file.write(
                f"{current_time} - Key: {request.key}, Value: {request.value}\n"
            )

        return replication_pb2.WriteResponse(
            ack=f"Write operation successful for {request.key}"
        )

    def send_heartbeat(self):
        """
        Periodically sends heartbeat messages to the ViewService to indicate the backup server's aliveness.
        """
        with grpc.insecure_channel("localhost:50053") as channel:
            stub = heartbeat_service_pb2_grpc.ViewServiceStub(channel)
            while True:
                try:
                    # Send a heartbeat message with the backup server's identifier.
                    stub.Heartbeat(
                        heartbeat_service_pb2.HeartbeatRequest(
                            service_identifier="backup"
                        )
                    )
                    print(
                        f"Heartbeat sent for backup at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    )
                except grpc.RpcError as e:
                    # Log any errors encountered while sending heartbeat messages.
                    print(f"Failed to send heartbeat: {str(e)}")
                time.sleep(5)  # Interval for sending heartbeat messages.


def serve():
    """
    Configures and starts the gRPC server, and schedules the sending of heartbeat messages.
    """
    backup_servicer = BackupSequenceServicer()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    replication_pb2_grpc.add_SequenceServicer_to_server(backup_servicer, server)
    server.add_insecure_port("[::]:50052")
    server.start()
    print("Backup server running on port 50052.")
    futures.ThreadPoolExecutor(max_workers=1).submit(backup_servicer.send_heartbeat)

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        # Handle server shutdown gracefully.
        print("Backup server shutting down.")
    finally:
        server.stop(None)


if __name__ == "__main__":
    serve()
