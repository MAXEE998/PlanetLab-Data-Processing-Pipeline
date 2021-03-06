# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: heartbeat.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='heartbeat.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0fheartbeat.proto\"4\n\tSendEntry\x12\n\n\x02to\x18\x01 \x01(\x05\x12\x0b\n\x03seq\x18\x02 \x01(\x03\x12\x0e\n\x06t_sent\x18\x03 \x01(\x03\"]\n\x0cReceiveEntry\x12\x0e\n\x06origin\x18\x01 \x01(\x05\x12\x0b\n\x03seq\x18\x02 \x01(\x03\x12\x0e\n\x06t_sent\x18\x03 \x01(\x03\x12\x12\n\nt_received\x18\x04 \x01(\x03\x12\x0c\n\x04hops\x18\x05 \x01(\x05\"&\n\x07SendLog\x12\x1b\n\x07\x65ntries\x18\x01 \x03(\x0b\x32\n.SendEntry\",\n\nReceiveLog\x12\x1e\n\x07\x65ntries\x18\x01 \x03(\x0b\x32\r.ReceiveEntryb\x06proto3'
)




_SENDENTRY = _descriptor.Descriptor(
  name='SendEntry',
  full_name='SendEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='to', full_name='SendEntry.to', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='seq', full_name='SendEntry.seq', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='t_sent', full_name='SendEntry.t_sent', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=19,
  serialized_end=71,
)


_RECEIVEENTRY = _descriptor.Descriptor(
  name='ReceiveEntry',
  full_name='ReceiveEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='origin', full_name='ReceiveEntry.origin', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='seq', full_name='ReceiveEntry.seq', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='t_sent', full_name='ReceiveEntry.t_sent', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='t_received', full_name='ReceiveEntry.t_received', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='hops', full_name='ReceiveEntry.hops', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=73,
  serialized_end=166,
)


_SENDLOG = _descriptor.Descriptor(
  name='SendLog',
  full_name='SendLog',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='entries', full_name='SendLog.entries', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=168,
  serialized_end=206,
)


_RECEIVELOG = _descriptor.Descriptor(
  name='ReceiveLog',
  full_name='ReceiveLog',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='entries', full_name='ReceiveLog.entries', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=208,
  serialized_end=252,
)

_SENDLOG.fields_by_name['entries'].message_type = _SENDENTRY
_RECEIVELOG.fields_by_name['entries'].message_type = _RECEIVEENTRY
DESCRIPTOR.message_types_by_name['SendEntry'] = _SENDENTRY
DESCRIPTOR.message_types_by_name['ReceiveEntry'] = _RECEIVEENTRY
DESCRIPTOR.message_types_by_name['SendLog'] = _SENDLOG
DESCRIPTOR.message_types_by_name['ReceiveLog'] = _RECEIVELOG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SendEntry = _reflection.GeneratedProtocolMessageType('SendEntry', (_message.Message,), {
  'DESCRIPTOR' : _SENDENTRY,
  '__module__' : 'heartbeat_pb2'
  # @@protoc_insertion_point(class_scope:SendEntry)
  })
_sym_db.RegisterMessage(SendEntry)

ReceiveEntry = _reflection.GeneratedProtocolMessageType('ReceiveEntry', (_message.Message,), {
  'DESCRIPTOR' : _RECEIVEENTRY,
  '__module__' : 'heartbeat_pb2'
  # @@protoc_insertion_point(class_scope:ReceiveEntry)
  })
_sym_db.RegisterMessage(ReceiveEntry)

SendLog = _reflection.GeneratedProtocolMessageType('SendLog', (_message.Message,), {
  'DESCRIPTOR' : _SENDLOG,
  '__module__' : 'heartbeat_pb2'
  # @@protoc_insertion_point(class_scope:SendLog)
  })
_sym_db.RegisterMessage(SendLog)

ReceiveLog = _reflection.GeneratedProtocolMessageType('ReceiveLog', (_message.Message,), {
  'DESCRIPTOR' : _RECEIVELOG,
  '__module__' : 'heartbeat_pb2'
  # @@protoc_insertion_point(class_scope:ReceiveLog)
  })
_sym_db.RegisterMessage(ReceiveLog)


# @@protoc_insertion_point(module_scope)
