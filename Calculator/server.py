import grpc
from concurrent import futures
import calculator_pb2
import calculator_pb2_grpc

class CalculatorServicer(calculator_pb2_grpc.CalculatorServicer):
    def Add(self, request, context):
        result = request.num1 + request.num2
        return calculator_pb2.AddResponse(result=result)
    
    def AddMult(self, request,context):
        add_result = request.num1 + request.num2
        mult_result = request.num1*request.num2
        aggregate_result = calculator_pb2.AddMultResponse(
           num1 = add_result,
           num2 = mult_result
        )
        return aggregate_result
  

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(CalculatorServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

