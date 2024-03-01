# Paramvir Sran, 251102997
# Code for a server that manages an inventory using gRPC and Redis

from concurrent import futures
import redis
import grpc
import inventory_pb2
import inventory_pb2_grpc
from threading import Lock


# The InventoryServiceServicer class is used to implement the service methods
class InventoryServiceServicer(inventory_pb2_grpc.InventoryServiceServicer):


    # The __init__ method is used to initialize the Redis connection.
    def __init__(self):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.lock = Lock()


    # The AddProduct method is used to add a product to the inventory.
    def AddProduct(self, request, context):
        print("AddProduct request:", request)

        with self.lock:
            if self.redis.hexists(str(request.product_identifier), 'product_name'):
                context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                context.set_details('Product already exists')
                return

            self.redis.hset(str(request.product_identifier), mapping={
                'product_name': str(request.product_name),
                'product_quantity': str(request.product_quantity),
                'product_price': str(request.product_price)
            })

            return inventory_pb2.Status(status='OK')


    # The GetProductById method is used to get a product from the inventory by its identifier.
    def GetProductById(self, request, context):
        print("GetProductById request:", request)

        product_info = self.redis.hgetall(str(request.product_identifier))

        if not product_info:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Product not found')
            return

        return inventory_pb2.Product(
            product_identifier=request.product_identifier,
            product_name=product_info[b'product_name'].decode('utf-8'),
            product_quantity=int(product_info[b'product_quantity']),
            product_price=float(product_info[b'product_price'])
        )


    # The UpdateProductQuantity method is used to update the quantity of a product in the inventory.
    def UpdateProductQuantity(self, request, context):
        print("UpdateProductQuantity request:", request)

        with self.lock:
            product_info = self.redis.hgetall(str(request.product_identifier))

            if not product_info:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Product not found')
                return

            self.redis.hset(str(request.product_identifier), mapping={'product_quantity': str(request.product_quantity)})
            product_info =  self.redis.hgetall(str(request.product_identifier))

            return inventory_pb2.Product(
                product_identifier=request.product_identifier,
                product_name=product_info[b'product_name'].decode('utf-8'),
                product_quantity=int(product_info[b'product_quantity']),
                product_price=float(product_info[b'product_price'])
            )


    # The DeleteProduct method is used to delete a product from the inventory.
    def DeleteProduct(self, request, context):
        print("DeleteProduct request:", request)

        with self.lock:
            if not self.redis.hexists(str(request.product_identifier), 'product_name'):
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Product not found')
                return
            else:
                self.redis.hdel(str(request.product_identifier), 'product_name', 'product_quantity', 'product_price')
                return inventory_pb2.Status(status='OK')


    # The GetAllProducts method is used to get a list of all products in the inventory
    def GetAllProducts(self, request, context):
        try:
            for key in self.redis.keys():
                if self.redis.type(key).decode('utf-8') != 'hash':
                    continue

                product_info = self.redis.hgetall(key)
                yield inventory_pb2.Product(
                    product_identifier=int(key),
                    product_name=product_info[b'product_name'].decode('utf-8'),
                    product_quantity=int(product_info[b'product_quantity']),
                    product_price=float(product_info[b'product_price'])
                )
        except Exception as e:
            print(e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Internal server error')
            return


def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    inventory_pb2_grpc.add_InventoryServiceServicer_to_server(InventoryServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Starting server. Listening on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    server()
