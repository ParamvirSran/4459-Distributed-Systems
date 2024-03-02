import GRPC
import replication_pb2.py
import replication_pb2_grpc.py
import heartbeat_service_pb2.py
import heartbeat_service_pb2_grpc.py
import time
import threading

port = 50051

# Primary class that implements the replication and heartbeat services and starts the server


class Primary(replication_pb2_grpc.ReplicationServicer):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.replica_list = []
        self.heartbeat_list = []
        self.heartbeat_thread = threading.Thread(target=self.heartbeat)
        self.heartbeat_thread.start()

        # Heartbeat function that checks the status of the replicas every 5 seconds
    def heartbeat(self):
        while True:
            for replica in self.replica_list:
                channel = GRPC.insecure_channel(replica.host, replica.port)
                stub = heartbeat_service_pb2_grpc.HeartbeatServiceStub(channel)
                response = stub.heartbeat(
                    heartbeat_service_pb2.HeartbeatRequest())
                if response.status == "down":
                    self.replica_list.remove(replica)
            time.sleep(5)

    def add_replica(self, request, context):
        self.replica_list.append(request)
        return replication_pb2.ReplicationResponse(status="success")

    def remove_replica(self, request, context):
        self.replica_list.remove(request)
        return replication_pb2.ReplicationResponse(status="success")

    def get_replica_list(self, request, context):
        return replication_pb2.ReplicaList(replica=self.replica_list)

    def add_heartbeat(self, request, context):
        self.heartbeat_list.append(request)
        return heartbeat_service_pb2.HeartbeatResponse(status="success")

    def remove_heartbeat(self, request, context):
        self.heartbeat_list.remove(request)
        return heartbeat_service_pb2.HeartbeatResponse(status="success")

    def get_heartbeat_list(self, request, context):
        return heartbeat_service_pb2.HeartbeatList(heartbeat=self.heartbeat_list)

    def start(self):
        server = GRPC.server()
        replication_pb2_grpc.add_ReplicationServicer_to_server(self, server)
        heartbeat_service_pb2_grpc.add_HeartbeatServiceServicer_to_server(
            self, server)
        server.add_insecure_port(self.host + ":" + self.port)
        server.start()
        server.wait_for_termination()


if __name__ == "__main__":

    primary = Primary("localhost", port)
    primary.start()
