import socket
import struct
from dataclasses import dataclass
from io import BytesIO
from typing import List

from dnsQuery import DNSHeader, DNSQuestion, build_query

TYPE_A = 1


@dataclass
class DNSRecord:
    name: bytes
    type_: int
    class_: int
    ttl: int
    data: bytes


@dataclass
class DNSPacket:
    header: DNSHeader
    questions: List[DNSQuestion]
    answers: List[DNSRecord]
    authorities: List[DNSRecord]
    additionals: List[DNSRecord]


def parse_header(reader):
    data = reader.read(12)
    id_, flags, num_questions, num_answers, num_authorities, num_additionals = (
        struct.unpack("!HHHHHH", data)
    )
    return DNSHeader(
        id_, flags, num_questions, num_answers, num_authorities, num_additionals
    )


def parse_question(reader):
    name = decode_name(reader)
    data = reader.read(4)
    type_, class_ = struct.unpack("!HH", data)
    return DNSQuestion(name, type_, class_)


def decode_name(reader):
    name = []
    while True:
        length = reader.read(1)[0]
        if length == 0:
            break
        if (length & 192) == 192:
            name.append(decode_compressed_name(length, reader))
            break
        name.append(reader.read(length).decode("ascii"))
    return ".".join(name)


def decode_compressed_name(length, reader):
    pointer_bytes = bytes([length & 63]) + reader.read(1)
    pointer = struct.unpack("!H", pointer_bytes)[0]
    current_pos = reader.tell()
    reader.seek(pointer)
    result = decode_name(reader)
    reader.seek(current_pos)
    return result


def parse_record(reader):
    name = decode_name(reader)
    data = reader.read(10)
    type_, class_, ttl, data_len = struct.unpack("!HHIH", data)
    if type_ == TYPE_A:
        data = reader.read(data_len)
    else:
        data = reader.read(data_len)
    return DNSRecord(name, type_, class_, ttl, data)


def parse_dns_packet(data):
    reader = BytesIO(data)
    header = parse_header(reader)
    questions = [parse_question(reader) for _ in range(header.num_questions)]
    answers = [parse_record(reader) for _ in range(header.num_answers)]
    authorities = [parse_record(reader) for _ in range(header.num_authorities)]
    additionals = [parse_record(reader) for _ in range(header.num_additionals)]
    return DNSPacket(header, questions, answers, authorities, additionals)


def ip_to_string(ip):
    return ".".join(str(byte) for byte in ip)


def lookup_domain(domain_name):
    query = build_query(domain_name, TYPE_A)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.sendto(query, ("localhost", 6969))
        response, _ = client_socket.recvfrom(1024)
        packet = parse_dns_packet(response)
        return packet.answers[0].data
