import random
import socket

from dnsParser import (
    DNSHeader,
    DNSPacket,
    DNSQuestion,
    DNSRecord,
    decode_name,
    ip_to_string,
    parse_dns_packet,
    parse_header,
    parse_question,
)
from dnsQuery import encode_dns_name, header_to_bytes, question_to_bytes

TYPE_TXT = 16
TYPE_A = 1
TYPE_NS = 2
import struct

CLASS_IN = 1
from io import BytesIO

nameserver = "198.41.0.4"
from dnsParser import decode_name, parse_header, parse_question


# build a dns query from a domain name and record type
def build_query(domain_name, record_type):
    name = encode_dns_name(domain_name)
    id = random.randint(0, 65535)
    header = DNSHeader(
        id=id,
        flags=0,
        num_questions=1,
        num_answers=0,
        num_authorities=0,
        num_additionals=0,
    )
    question = DNSQuestion(name, record_type, CLASS_IN)
    return header_to_bytes(header) + question_to_bytes(question)


# send a dns query to a nameserver and return the response
def send_query(ip_address, domain_name, record_type):
    query = build_query(domain_name, record_type)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.sendto(query, (ip_address, 53))
        response, _ = client_socket.recvfrom(1024)
        return parse_dns_packet(response)


# parse a dns record from raw bytes (used for parsing answers, authorities, and additionals)
def parse_record(reader):
    name = decode_name(reader)
    data = reader.read(10)
    type_, class_, ttl, data_len = struct.unpack("!HHIH", data)
    if type_ == TYPE_A:
        data = reader.read(data_len)
    else:
        data = reader.read(data_len)
    return DNSRecord(name, type_, class_, ttl, data)


# parse a dns packet from raw bytes
def parse_dns_packet(data):
    reader = BytesIO(data)
    header = parse_header(reader)
    questions = [parse_question(reader) for _ in range(header.num_questions)]
    answers = [parse_record(reader) for _ in range(header.num_answers)]
    authorities = [parse_record(reader) for _ in range(header.num_authorities)]
    additionals = [parse_record(reader) for _ in range(header.num_additionals)]
    return DNSPacket(header, questions, answers, authorities, additionals)


def get_answer(packet):
    for x in packet.answers:
        if x.type_ == TYPE_A:
            return ip_to_string(x.data)


def get_nameserver_ip(packet):
    for x in packet.authorities:
        if x.type_ == TYPE_A:
            return ip_to_string(x.data)


def get_nameserver(packet):
    for x in packet.authorities:
        if x.type_ == TYPE_NS:
            return x.data


def resolve(domain_name, record_type):
    # Assuming 'nameserver' is initialized earlier or passed as an argument
    # This simplified example needs to be expanded based on actual logic for iterating NS records
    response = send_query(nameserver, domain_name, record_type)
    if response.header.flags & 0x0F == 3:
        # NXDOMAIN, domain does not exist
        return None
    elif response.answers:
        # Found an answer, return the first A record's IP
        for answer in response.answers:
            if answer.type_ == TYPE_A:
                return ip_to_string(answer.data)
    # Additional handling for other cases
    return None


def serialize_dns_response(request, ip):
    writer = BytesIO()
    writer.write(header_to_bytes(request.header))  # Copy request header to response
    for question in request.questions:
        writer.write(question_to_bytes(question))  # Include question in response
    if ip:
        ip_bytes = socket.inet_aton(ip)
        answer_section = struct.pack("!HHIH", TYPE_A, CLASS_IN, 300, 4) + ip_bytes
        writer.write(answer_section)
    else:
        # Modify response header for error, e.g., NXDOMAIN (name does not exist)
        # This example directly manipulates 'writer' which may not reflect actual header modifications
        # Consider adjusting the header flags to indicate an error
        pass
    return writer.getvalue()


def main():
    server_address = "localhost"
    server_port = 6969

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((server_address, server_port))
        print(f"Listening on {server_address}:{server_port}")

        while True:
            data, addr = server_socket.recvfrom(1024)
            print(f"Received query from {addr}")
            print(data)

            try:
                request = parse_dns_packet(data)
                print(f"Parsed query: {request}")

                domain_name = request.questions[0].name
                print(f"Received query for {domain_name}")

                record_type = request.questions[0].type_
                print(f"Received query for {record_type}")
                print("here")

                ip = resolve(domain_name, record_type)
                print(f"Resolved to {ip}")

                response = serialize_dns_response(request, ip)
                server_socket.sendto(response, addr)
                print(f"Sent response to {addr}")
            except Exception as e:
                print(f"Error: {e}")
                server_socket.sendto(b"\x00", addr)
                print(f"Sent error response to {addr}")
                continue


if __name__ == "__main__":
    main()
