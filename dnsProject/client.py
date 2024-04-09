# Paramvir Sran, 251102997

import datetime

import grpc

import replication_pb2
import replication_pb2_grpc


def log_operation(operation, file_name="client.txt"):
    """
    Logs client operations and server responses or errors, along with a timestamp,
    to provide a comprehensive record of interactions with the primary server.
    """
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_name, "a") as log_file:
        log_file.write(f"{current_time} - {operation}\n")


def run():
    """
    Main function to interact with the primary server.
    Handles user input for key-value pairs and communicates with the server
    to execute write operations. Errors and server responses are logged and printed.
    """
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
                # Sends a write request to the primary server and logs the response
                response = stub.Write(
                    replication_pb2.WriteRequest(key=key, value=value)
                )
                print(f"Server responded: {response.ack}")
                log_operation(
                    f"Write request - Key: {key}, Value: {value}. Server ACK: {response.ack}"
                )
            except grpc.RpcError as e:
                # Handles RPC errors by logging detailed error information
                error_message = f"An error occurred: {e.code()} - {e.details()}"
                print(error_message)
                log_operation(
                    f"Error during write request - Key: {key}, Value: {value}. {error_message}"
                )


if __name__ == "__main__":
    run()
