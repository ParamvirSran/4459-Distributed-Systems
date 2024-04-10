import dataclasses
import random

TYPE_A = 1
CLASS_IN = 1
import struct
from dataclasses import dataclass


@dataclass
class DNSHeader:
    id: int
    flags: int
    num_questions: int
    num_answers: int
    num_authorities: int
    num_additionals: int


@dataclass
class DNSQuestion:
    name: bytes
    type_: int
    class_: int


def header_to_bytes(header):
    return struct.pack(
        "!HHHHHH",
        header.id,
        header.flags,
        header.num_questions,
        header.num_answers,
        header.num_authorities,
        header.num_additionals,
    )


def question_to_bytes(question):
    return question.name + struct.pack("!HH", question.type_, question.class_)


def encode_dns_name(domain_name):
    return (
        b"".join(
            struct.pack("B", len(label)) + label.encode("ascii")
            for label in domain_name.split(".")
        )
        + b"\x00"
    )


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
    question = DNSQuestion(name=name, type_=record_type, class_=CLASS_IN)
    return header_to_bytes(header) + question_to_bytes(question)
