# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: deep.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='deep.proto',
  package='org.libcppa',
  syntax='proto2',
  serialized_pb=_b('\n\ndeep.proto\x12\x0borg.libcppa\">\n\ninput_pack\x12\x0c\n\x04size\x18\x01 \x01(\x05\x12\"\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32\x14.org.libcppa.input_m\"@\n\x0boutput_pack\x12\x0c\n\x04size\x18\x01 \x01(\x05\x12#\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32\x15.org.libcppa.output_m\"\xc3\x01\n\x07input_m\x12\x0f\n\x07version\x18\x01 \x01(\t\x12\x36\n\x06method\x18\x02 \x01(\x0e\x32\x1f.org.libcppa.input_m.methodType:\x05\x43\x41\x46\x46\x45\x12.\n\x05\x64\x61taT\x18\x03 \x01(\x0e\x32\x15.org.libcppa.dataType:\x08\x43V_IMAGE\x12\x0f\n\x07imgdata\x18\x04 \x01(\x0c\".\n\nmethodType\x12\x0b\n\x07\x43V_FLIP\x10\x00\x12\t\n\x05\x43\x41\x46\x46\x45\x10\x01\x12\x08\n\x04YOLO\x10\x02\"\x89\x01\n\x08output_m\x12#\n\x06status\x18\x01 \x01(\x0e\x32\x13.org.libcppa.Status\x12\x0b\n\x03msg\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\t\x12)\n\x05\x64\x61taT\x18\x04 \x01(\x0e\x32\x15.org.libcppa.dataType:\x03PNG\x12\x0f\n\x07imgdata\x18\x05 \x01(\x0c*!\n\x08\x64\x61taType\x12\x07\n\x03PNG\x10\x00\x12\x0c\n\x08\x43V_IMAGE\x10\x01*e\n\x06Status\x12\x06\n\x02OK\x10\x00\x12\x0b\n\x07INVALID\x10\x01\x12\x10\n\x0cWRONG_METHOD\x10\x02\x12\x12\n\x0eWRONG_DATATYPE\x10\x03\x12\x10\n\x0cTOO_BIG_DATA\x10\x04\x12\x0e\n\nSEVER_FAIL\x10\x05')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

_DATATYPE = _descriptor.EnumDescriptor(
  name='dataType',
  full_name='org.libcppa.dataType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='PNG', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CV_IMAGE', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=495,
  serialized_end=528,
)
_sym_db.RegisterEnumDescriptor(_DATATYPE)

dataType = enum_type_wrapper.EnumTypeWrapper(_DATATYPE)
_STATUS = _descriptor.EnumDescriptor(
  name='Status',
  full_name='org.libcppa.Status',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='OK', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WRONG_METHOD', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WRONG_DATATYPE', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TOO_BIG_DATA', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SEVER_FAIL', index=5, number=5,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=530,
  serialized_end=631,
)
_sym_db.RegisterEnumDescriptor(_STATUS)

Status = enum_type_wrapper.EnumTypeWrapper(_STATUS)
PNG = 0
CV_IMAGE = 1
OK = 0
INVALID = 1
WRONG_METHOD = 2
WRONG_DATATYPE = 3
TOO_BIG_DATA = 4
SEVER_FAIL = 5


_INPUT_M_METHODTYPE = _descriptor.EnumDescriptor(
  name='methodType',
  full_name='org.libcppa.input_m.methodType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='CV_FLIP', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CAFFE', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='YOLO', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=307,
  serialized_end=353,
)
_sym_db.RegisterEnumDescriptor(_INPUT_M_METHODTYPE)


_INPUT_PACK = _descriptor.Descriptor(
  name='input_pack',
  full_name='org.libcppa.input_pack',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='size', full_name='org.libcppa.input_pack.size', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data', full_name='org.libcppa.input_pack.data', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=27,
  serialized_end=89,
)


_OUTPUT_PACK = _descriptor.Descriptor(
  name='output_pack',
  full_name='org.libcppa.output_pack',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='size', full_name='org.libcppa.output_pack.size', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data', full_name='org.libcppa.output_pack.data', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=91,
  serialized_end=155,
)


_INPUT_M = _descriptor.Descriptor(
  name='input_m',
  full_name='org.libcppa.input_m',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='org.libcppa.input_m.version', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='method', full_name='org.libcppa.input_m.method', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dataT', full_name='org.libcppa.input_m.dataT', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='imgdata', full_name='org.libcppa.input_m.imgdata', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _INPUT_M_METHODTYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=158,
  serialized_end=353,
)


_OUTPUT_M = _descriptor.Descriptor(
  name='output_m',
  full_name='org.libcppa.output_m',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='org.libcppa.output_m.status', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='msg', full_name='org.libcppa.output_m.msg', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='version', full_name='org.libcppa.output_m.version', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dataT', full_name='org.libcppa.output_m.dataT', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='imgdata', full_name='org.libcppa.output_m.imgdata', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=356,
  serialized_end=493,
)

_INPUT_PACK.fields_by_name['data'].message_type = _INPUT_M
_OUTPUT_PACK.fields_by_name['data'].message_type = _OUTPUT_M
_INPUT_M.fields_by_name['method'].enum_type = _INPUT_M_METHODTYPE
_INPUT_M.fields_by_name['dataT'].enum_type = _DATATYPE
_INPUT_M_METHODTYPE.containing_type = _INPUT_M
_OUTPUT_M.fields_by_name['status'].enum_type = _STATUS
_OUTPUT_M.fields_by_name['dataT'].enum_type = _DATATYPE
DESCRIPTOR.message_types_by_name['input_pack'] = _INPUT_PACK
DESCRIPTOR.message_types_by_name['output_pack'] = _OUTPUT_PACK
DESCRIPTOR.message_types_by_name['input_m'] = _INPUT_M
DESCRIPTOR.message_types_by_name['output_m'] = _OUTPUT_M
DESCRIPTOR.enum_types_by_name['dataType'] = _DATATYPE
DESCRIPTOR.enum_types_by_name['Status'] = _STATUS

input_pack = _reflection.GeneratedProtocolMessageType('input_pack', (_message.Message,), dict(
  DESCRIPTOR = _INPUT_PACK,
  __module__ = 'deep_pb2'
  # @@protoc_insertion_point(class_scope:org.libcppa.input_pack)
  ))
_sym_db.RegisterMessage(input_pack)

output_pack = _reflection.GeneratedProtocolMessageType('output_pack', (_message.Message,), dict(
  DESCRIPTOR = _OUTPUT_PACK,
  __module__ = 'deep_pb2'
  # @@protoc_insertion_point(class_scope:org.libcppa.output_pack)
  ))
_sym_db.RegisterMessage(output_pack)

input_m = _reflection.GeneratedProtocolMessageType('input_m', (_message.Message,), dict(
  DESCRIPTOR = _INPUT_M,
  __module__ = 'deep_pb2'
  # @@protoc_insertion_point(class_scope:org.libcppa.input_m)
  ))
_sym_db.RegisterMessage(input_m)

output_m = _reflection.GeneratedProtocolMessageType('output_m', (_message.Message,), dict(
  DESCRIPTOR = _OUTPUT_M,
  __module__ = 'deep_pb2'
  # @@protoc_insertion_point(class_scope:org.libcppa.output_m)
  ))
_sym_db.RegisterMessage(output_m)


# @@protoc_insertion_point(module_scope)