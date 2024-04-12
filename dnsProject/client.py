# 4459 Group Project - DNS Resolver
# Client script that sends requests to the server to resolve domain names

import socket

import dns

# server address and port
server_address = "localhost"
server_port = 3599

# record types
TYPE_A = 1
TYPE_NS = 2


# main function to get domain name from user and send it to the server
def main():
    print('\nFormat of domain name is: "google.com"')
    domain = input("Enter domain name or 'exit': ")

    # while the user does not input "exit", keep asking for a domain name
    while domain.lower() != "exit":
        # Create a UDP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Create a DNS query
        query = dns.build_query(domain, TYPE_A)

        # Send the query to the server
        client_socket.sendto(query, (server_address, server_port))

        # Receive the response from the server
        response, _ = client_socket.recvfrom(1024)

        # convert ip address from bytes to string
        str_response = dns.ip_to_string(response)

        # if the ip address was not resolved by server print an error message else print the ip address
        if str_response == "0.0.0.0":
            print(f"Could not resolve {domain}")
        else:
            print(str_response)

        client_socket.close()  # close the socket

        print('\nFormat of domain name is: "google.com"')
        domain = input("Enter domain name or 'exit': ")

    print("Exiting...")


if __name__ == "__main__":
    main()
