# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: replication.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11replication.proto\x12\x0breplication\"*\n\x0cWriteRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"\x1c\n\rWriteResponse\x12\x0b\n\x03\x61\x63k\x18\x01 \x01(\t2J\n\x08Sequence\x12>\n\x05Write\x12\x19.replication.WriteRequest\x1a\x1a.replication.WriteResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'replication_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_WRITEREQUEST']._serialized_start=34
  _globals['_WRITEREQUEST']._serialized_end=76
  _globals['_WRITERESPONSE']._serialized_start=78
  _globals['_WRITERESPONSE']._serialized_end=106
  _globals['_SEQUENCE']._serialized_start=108
  _globals['_SEQUENCE']._serialized_end=182
# @@protoc_insertion_point(module_scope)
