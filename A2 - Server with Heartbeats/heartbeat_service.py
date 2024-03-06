import logging
import time
from concurrent import futures

import grpc
from google.protobuf import empty_pb2

import heartbeat_service_pb2
import heartbeat_service_pb2_grpc

logging.basicConfig(level=logging.INFO, filename="heartbeat.txt", filemode="a")


class ViewService(heartbeat_service_pb2_grpc.ViewServiceServicer):
    def __init__(self):
        self.last_heartbeat = {}
        self.reported_down = set()  # Track servers reported as down

    def Heartbeat(self, request, context):
        service_identifier = request.service_identifier
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.last_heartbeat[service_identifier] = time.time()
        if service_identifier in self.reported_down:
            self.reported_down.remove(service_identifier)  # Server is back up
            logging.info(
                f"{service_identifier.capitalize()} is back up as of [{current_time}]."
            )
        else:
            logging.info(
                f"{service_identifier.capitalize()} is alive. Latest heartbeat received at [{current_time}]."
            )
        return empty_pb2.Empty()

    def monitor_heartbeats(self):
        while True:
            current_time = time.time()
            for service_identifier, last_time in self.last_heartbeat.items():
                if (
                    current_time - last_time > 5
                    and service_identifier not in self.reported_down
                ):
                    logging.info(
                        f"{service_identifier.capitalize()} might be down. No heartbeat since [{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_time))}]."
                    )
                    self.reported_down.add(service_identifier)
            time.sleep(5)


def serve():
    vs = ViewService()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    heartbeat_service_pb2_grpc.add_ViewServiceServicer_to_server(vs, server)
    server.add_insecure_port("[::]:50053")
    try:
        server.start()
        print("Heartbeat server started on port 50053.")
        futures.ThreadPoolExecutor(max_workers=1).submit(vs.monitor_heartbeats)
        server.wait_for_termination()
    except Exception as e:
        logging.error(f"Failed to start the heartbeat server: {str(e)}")


if __name__ == "__main__":
    serve()
