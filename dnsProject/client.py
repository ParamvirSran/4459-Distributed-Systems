import socket

# Assuming dnsQuery.py is available for building queries
import dnsQuery

TYPE_A = 1
server_address = "localhost"
server_port = 6969
domain_name = "example.com"
record_type = TYPE_A


def main():
    # Prepare the DNS query
    query = dnsQuery.build_query(domain_name, record_type)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        # Send the DNS query to the server
        client_socket.sendto(query, (server_address, server_port))

        # Receive the response from the server
        data, addr = client_socket.recvfrom(1024)

        # Simply print the raw response data
        # Normally, the client should parse this data to read the response,
        # but parsing DNS packets is non-trivial and typically handled by libraries
        print(f"Received response from {addr}")
        print(f"Response: {data}")

        # The client generally wouldn't perform DNS resolution itself
        # or attempt to parse the DNS response packet directly without a library.
        # Instead, it would use higher-level libraries or system calls for such tasks.


if __name__ == "__main__":
    main()
