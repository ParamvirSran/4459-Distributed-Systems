# 4459 Group Project - DNS Resolver
# Server script that listens for incoming requests to resolve domain names

import dataclasses
import random
import socket
import struct
from dataclasses import dataclass
from io import BytesIO
from typing import List

# record types
TYPE_A = 1  # Address record type (IPv4 address)
TYPE_NS = 2  # Name server record type (domain name)
CLASS_IN = 1  # Internet class of addresses
TYPE_TXT = 16  # Text strings

# server address and port
port = 3599
address = "localhost"


# DNS Header (id, flags, num_questions, num_answers, num_authorities, num_additionals)
@dataclass
class DNSHeader:
    id: int
    flags: int
    num_questions: int = 0
    num_answers: int = 0
    num_authorities: int = 0
    num_additionals: int = 0


# DNS Question (name, type, class)
@dataclass
class DNSQuestion:
    name: bytes
    type_: int
    class_: int


# DNS Record (name, type, class, ttl, data)
@dataclass
class DNSRecord:
    name: bytes
    type_: int
    class_: int
    ttl: int
    data: bytes


# DNS Packet (header, questions, answers, authorities, additionals)
@dataclass
class DNSPacket:
    header: DNSHeader
    questions: List[DNSQuestion]
    answers: List[DNSRecord]
    authorities: List[DNSRecord]
    additionals: List[DNSRecord]


# convert header to bytes
def header_to_bytes(header):
    fields = dataclasses.astuple(header)
    return struct.pack("!HHHHHH", *fields)


# convert question to bytes
def question_to_bytes(question):
    return question.name + struct.pack("!HH", question.type_, question.class_)


# encode a domain name to bytes to send over the network
def encode_dns_name(domain_name):
    encoded = b""
    for part in domain_name.encode("ascii").split(b"."):
        encoded += bytes([len(part)]) + part
    return encoded + b"\x00"


# parse a header from the reader and return a DNSHeader object
def parse_header(reader):
    items = struct.unpack("!HHHHHH", reader.read(12))
    return DNSHeader(*items)


# parse a question from the reader and return a DNSQuestion object
def parse_question(reader):
    name = decode_name(reader)
    data = reader.read(4)
    type_, class_ = struct.unpack("!HH", data)
    return DNSQuestion(name, type_, class_)


# decode the domain name from the reader and return the domain name
def decode_name(reader):
    parts = []
    while (length := reader.read(1)[0]) != 0:
        if length & 192:
            parts.append(
                decode_compressed_name(length, reader)
            )  # compressed name if length is 192
            break
        else:
            parts.append(reader.read(length))
    return b".".join(parts)


# decode a compressed name from the reader and return the domain name
def decode_compressed_name(length, reader):
    pointer_bytes = bytes([length & 63]) + reader.read(1)
    pointer = struct.unpack("!H", pointer_bytes)[0]
    current_pos = reader.tell()
    reader.seek(pointer)
    result = decode_name(reader)
    reader.seek(current_pos)
    return result


# convert an ip address to a string
def ip_to_string(ip):
    return ".".join([str(x) for x in ip])


# lookup the domain name using the Google DNS server and return the ip address
def lookup_domain(domain_name):
    query = build_query(domain_name, TYPE_A)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(query, ("8.8.8.8", 53))
    data, _ = sock.recvfrom(1024)
    response = parse_dns_packet(data)
    return ip_to_string(response.answers[0].data)


# build a DNS query for the given domain name and record type
def build_query(domain_name, record_type):
    name = encode_dns_name(domain_name)
    id = random.randint(0, 65535)
    header = DNSHeader(id=id, num_questions=1, flags=0)
    question = DNSQuestion(name=name, type_=record_type, class_=CLASS_IN)
    return header_to_bytes(header) + question_to_bytes(question)


# send a query to the given ip address for the domain name and record type
def send_query(ip_address, domain_name, record_type):
    query = build_query(domain_name, record_type)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(query, (ip_address, 53))
    data, _ = sock.recvfrom(1024)
    return parse_dns_packet(data)


# parse a record from the reader and return a DNSRecord object
def parse_record(reader):
    name = decode_name(reader)
    data = reader.read(10)
    type_, class_, ttl, data_len = struct.unpack("!HHIH", data)
    if type_ == TYPE_NS:
        data = decode_name(reader)
    elif type_ == TYPE_A:
        data = ip_to_string(reader.read(data_len))
    else:
        data = reader.read(data_len)
    return DNSRecord(name, type_, class_, ttl, data)


# parse a DNS packet from the data and return a DNSPacket object
def parse_dns_packet(data):
    reader = BytesIO(data)
    header = parse_header(reader)
    questions = [parse_question(reader) for _ in range(header.num_questions)]
    answers = [parse_record(reader) for _ in range(header.num_answers)]
    authorities = [parse_record(reader) for _ in range(header.num_authorities)]
    additionals = [parse_record(reader) for _ in range(header.num_additionals)]
    return DNSPacket(header, questions, answers, authorities, additionals)


# get the answer from the packet if it exists and return the ip address
def get_answer(packet):
    for x in packet.answers:
        if x.type_ == TYPE_A:
            return x.data


# get the nameserver ip from the packet if it exists and return the ip address
def get_nameserver_ip(packet):
    for x in packet.additionals:
        if x.type_ == TYPE_A:
            return x.data


# get the nameserver from the packet if it exists and return the domain name
def get_nameserver(packet):
    for x in packet.authorities:
        if x.type_ == TYPE_NS:
            return x.data.decode("utf-8")


# resolve the domain name by querying the root nameserver and return the ip address
def resolve(domain_name, record_type):
    nameserver = "198.41.0.4"  # root nameserver ip address (a.root-servers.net)
    timeout = 0  # timeout counter to prevent infinite loop if the domain is not found

    # while the ip address is not found keep recursively querying the nameservers
    while True:
        timeout += 1
        print(f"Querying {nameserver} for {domain_name} ({record_type})")
        response = send_query(nameserver, domain_name, record_type)

        # conditions to check if the answer, nameserver ip or nameserver is found
        if ip := get_answer(response):  # if the answer is found return the ip
            return ip
        elif nsIP := get_nameserver_ip(
            response
        ):  # if the nameserver ip is found query the nameserver
            nameserver = nsIP
        elif ns_domain := get_nameserver(
            response
        ):  # if the nameserver is found query the nameserver
            nameserver = resolve(ns_domain, TYPE_A)

        else:  # if no answer or nameserver is found raise an exception
            raise Exception("Problem Resolving Domain")
        if timeout > 10:  # if the timeout is greater than 10 raise an exception
            raise Exception("Problem Resolving Domain")


# convert an ip address to bytes to send over the network
def ip_to_bytes(ip_address):
    try:
        return socket.inet_aton(ip_address)
    except socket.error as e:
        raise ValueError(f"Invalid IP address '{ip_address}': {e}")


# main function to listen for incoming requests and resolve domain names to ip addresses and send them back to the client
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create a UDP socket
    server.bind((address, port))  # bind the socket to the address and port
    print(f"DNS server listening on {address}:{port}")

    # while the server is running keep listening for incoming requests
    while True:
        print("\n")
        data, addr = server.recvfrom(
            1024
        )  # receive the data and address from the client

        try:
            request = parse_dns_packet(data)  # parse the request
            query = request.questions[0]  # get the first question from the request
            domain_name = query.name.decode("ascii")  # decode the domain name
            record_type = query.type_  # get the record type
            print(f"Received query for {domain_name} ({record_type}) from {addr}")

            # resolve the domain name and get the ip address of the domain
            ip_address = resolve(domain_name, record_type)
            print(f"Resolved {domain_name} to {ip_address}")

            # send the ip address back to the client in bytes
            ipBytes = ip_to_bytes(ip_address)
            server.sendto(ipBytes, addr)

        # if an error occurs send an error message back to the client with ip address 'None'
        except Exception as e:
            print(f"Error: {e}")
            ipBytes = ip_to_bytes("0.0.0.0")
            server.sendto(ipBytes, addr)


if __name__ == "__main__":
    main()
