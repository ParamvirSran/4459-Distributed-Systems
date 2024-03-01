# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import streaming_pb2 as streaming__pb2


class ServerToClientStreamingExampleStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.StreamMessages = channel.unary_stream(
                '/ServerToClientStreamingExample/StreamMessages',
                request_serializer=streaming__pb2.Empty.SerializeToString,
                response_deserializer=streaming__pb2.Message.FromString,
                )


class ServerToClientStreamingExampleServicer(object):
    """Missing associated documentation comment in .proto file."""

    def StreamMessages(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ServerToClientStreamingExampleServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'StreamMessages': grpc.unary_stream_rpc_method_handler(
                    servicer.StreamMessages,
                    request_deserializer=streaming__pb2.Empty.FromString,
                    response_serializer=streaming__pb2.Message.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ServerToClientStreamingExample', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ServerToClientStreamingExample(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def StreamMessages(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/ServerToClientStreamingExample/StreamMessages',
            streaming__pb2.Empty.SerializeToString,
            streaming__pb2.Message.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)