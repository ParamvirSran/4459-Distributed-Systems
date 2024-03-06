import datetime

import grpc

import replication_pb2
import replication_pb2_grpc


def log_operation(operation, file_name="client.txt"):
    """Log operations and errors to the specified file with timestamps."""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_name, "a") as log_file:
        log_file.write(f"{current_time} - {operation}\n")


def run():
    """Interact with the primary server to send write requests."""
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = replication_pb2_grpc.SequenceStub(channel)

        while True:
            key = input("Enter key (or 'exit' to quit): ").strip()
            if key.lower() == "exit":
                print("Exiting client...")
                break

            value = input("Enter value: ").strip()
            if not key or not value:
                print("Both key and value must be non-empty. Please try again.")
                continue

            try:
                response = stub.Write(
                    replication_pb2.WriteRequest(key=key, value=value)
                )
                print(f"Server responded: {response.ack}")
                log_operation(
                    f"Write request - Key: {key}, Value: {value}. Server ACK: {response.ack}"
                )
            except grpc.RpcError as e:
                error_message = f"An error occurred: {e.code()} - {e.details()}"
                print(error_message)
                log_operation(
                    f"Error during write request - Key: {key}, Value: {value}. {error_message}"
                )


if __name__ == "__main__":
    run()
