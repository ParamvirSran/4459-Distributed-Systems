# Paramvir Sran, 251102997
# client implementation to call the inventory service methods from the server using gRPC

import grpc
import inventory_pb2
import inventory_pb2_grpc
from google.protobuf import empty_pb2


# The run function is used to call the service methods
def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = inventory_pb2_grpc.InventoryServiceStub(channel)

        # get all products
        print('requesting all products')
        responses = stub.GetAllProducts(empty_pb2.Empty())

        for response in responses:
            print('Received product:', response)

        # AddProduct test
        response = stub.AddProduct(inventory_pb2.Product(
            product_identifier=1,
            product_name='Apple',
            product_quantity=10,
            product_price=1.5
        ))
        print('AddProduct', response)

        # GetProductById test
        response = stub.GetProductById(inventory_pb2.ProductIdentifier(product_identifier=1))
        print('GetProductById', response)

        # UpdateProductQuantity test
        response = stub.UpdateProductQuantity(inventory_pb2.Quantity(
            product_identifier=1,
            product_quantity=20
        ))
        print('UpdateProductQuantity', response)

        # DeleteProduct test
        response = stub.DeleteProduct(inventory_pb2.ProductIdentifier(product_identifier=1))
        print('DeleteProduct', response)

        # add three more products
        response = stub.AddProduct(inventory_pb2.Product(
            product_identifier=2,
            product_name='Banana',
            product_quantity=10,
            product_price=1.5
        ))
        print('AddProduct', response)

        response = stub.AddProduct(inventory_pb2.Product(
            product_identifier=3,
            product_name='Orange',
            product_quantity=10,
            product_price=1.5
        ))
        print('AddProduct', response)

        response = stub.AddProduct(inventory_pb2.Product(
            product_identifier=4,
            product_name='Grapes',
            product_quantity=10,
            product_price=1.5
        ))
        print('AddProduct', response)

        # GetAllProducts test
        print('requesting all products')
        responses = stub.GetAllProducts(empty_pb2.Empty())

        for response in responses:
            print('Received product:', response)

        # delete 2,3,4
        response = stub.DeleteProduct(inventory_pb2.ProductIdentifier(product_identifier=2))
        print('DeleteProduct', response)

        response = stub.DeleteProduct(inventory_pb2.ProductIdentifier(product_identifier=3))
        print('DeleteProduct', response)

        response = stub.DeleteProduct(inventory_pb2.ProductIdentifier(product_identifier=4))
        print('DeleteProduct', response)


if __name__ == '__main__':
    run()
