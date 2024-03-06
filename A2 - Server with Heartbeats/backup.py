import datetime
import time
from concurrent import futures

import grpc

import heartbeat_service_pb2
import heartbeat_service_pb2_grpc
import replication_pb2
import replication_pb2_grpc


class BackupSequenceServicer(replication_pb2_grpc.SequenceServicer):
    def __init__(self):
        self.data = {}  # Data store for key-value pairs

    def Write(self, request, context):
        # Validate input
        if not request.key or not request.value:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Key and value cannot be empty.")
            return replication_pb2.WriteResponse(
                ack="Invalid request: Empty key or value."
            )

        # Perform the write operation
        self.data[request.key] = request.value

        # Log the operation with timestamp
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("backup.txt", "a") as log_file:
            log_file.write(
                f"{current_time} - Key: {request.key}, Value: {request.value}\n"
            )

        return replication_pb2.WriteResponse(
            ack=f"Write operation successful for {request.key}"
        )

    def send_heartbeat(self):
        with grpc.insecure_channel("localhost:50053") as channel:
            stub = heartbeat_service_pb2_grpc.ViewServiceStub(channel)
            while True:
                try:
                    stub.Heartbeat(
                        heartbeat_service_pb2.HeartbeatRequest(
                            service_identifier="backup"
                        )
                    )
                    print(
                        f"Heartbeat sent for backup at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    )
                except grpc.RpcError as e:
                    print(f"Failed to send heartbeat: {str(e)}")
                time.sleep(5)  # Send heartbeat every 5 seconds


def serve():
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
        print("Backup server shutting down.")
    finally:
        server.stop(None)  # Ensure a graceful shutdown


if __name__ == "__main__":
    serve()
