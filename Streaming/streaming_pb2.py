# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: streaming.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fstreaming.proto\"\x1a\n\x07Message\x12\x0f\n\x07\x63ontent\x18\x01 \x01(\t\"\x07\n\x05\x45mpty2F\n\x1eServerToClientStreamingExample\x12$\n\x0eStreamMessages\x12\x06.Empty\x1a\x08.Message0\x01\x62\x06proto3')



_MESSAGE = DESCRIPTOR.message_types_by_name['Message']
_EMPTY = DESCRIPTOR.message_types_by_name['Empty']
Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), {
  'DESCRIPTOR' : _MESSAGE,
  '__module__' : 'streaming_pb2'
  # @@protoc_insertion_point(class_scope:Message)
  })
_sym_db.RegisterMessage(Message)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'streaming_pb2'
  # @@protoc_insertion_point(class_scope:Empty)
  })
_sym_db.RegisterMessage(Empty)

_SERVERTOCLIENTSTREAMINGEXAMPLE = DESCRIPTOR.services_by_name['ServerToClientStreamingExample']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MESSAGE._serialized_start=19
  _MESSAGE._serialized_end=45
  _EMPTY._serialized_start=47
  _EMPTY._serialized_end=54
  _SERVERTOCLIENTSTREAMINGEXAMPLE._serialized_start=56
  _SERVERTOCLIENTSTREAMINGEXAMPLE._serialized_end=126
# @@protoc_insertion_point(module_scope)
