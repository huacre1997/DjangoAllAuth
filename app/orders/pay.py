from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment

import sys

class PayPalClient:
    def __init__(self):
        self.client_id = "AYRJdMjOMSHzkclga9bXdSKPbE7lxUApV34JV7WpvOWcmVBBRfneP7n2q-__8UX0gcHx_8SrRThjVhGu"
        self.client_secret = "EAFWjp4J4g10tt9Ku7gw1kBPvvdPpGHnZIjN294eiAt0nnQNbP3x6ELFtObjxCcOnSG5J5ixKkNsnolc"


        """Set up and return PayPal Python SDK environment with PayPal access credentials.
           This sample uses SandboxEnvironment. In production, use LiveEnvironment."""

        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)

        """ Returns PayPal HTTP client instance with environment that has access
            credentials context. Use this instance to invoke PayPal APIs, provided the
            credentials have access. """
        self.client = PayPalHttpClient(self.environment)

    def object_to_json(self, json_data):
        """
        Function to print all json data in an organized readable manner
        """
        result = {}
        if sys.version_info[0] < 3:
            itr = json_data.__dict__.iteritems()
        else:
            itr = json_data.__dict__.items()
        for key,value in itr:
            # Skip internal attributes.
            if key.startswith("__"):
                continue
            result[key] = self.array_to_json_array(value) if isinstance(value, list) else\
                        self.object_to_json(value) if not self.is_primittive(value) else\
                         value
        return result
    def array_to_json_array(self, json_array):
        result =[]
        if isinstance(json_array, list):
            for item in json_array:
                result.append(self.object_to_json(item) if  not self.is_primittive(item) else\
                         self.array_to_json_array(item) if isinstance(item, list) else item)
        return result

    def is_primittive(self, data):
        return isinstance(data, str) or isinstance(data, unicode) or isinstance(data, int)
from paypalcheckoutsdk.orders import OrdersGetRequest

class GetOrder(PayPalClient):

  #2. Set up your server to receive a call from the client
  
    def get_order(self, order_id):
        request = OrdersGetRequest(order_id)
        #3. Call PayPal to get the transaction
        response = self.client.execute(request)
        print(response.result)
        print ('Status Code: ', response.status_code)
        print ('Status: ', response.result.status)
        print('Order ID: ', response.result.id)
        print('Intent: ', response.result.intent)
        print ('Links:')
        for link in response.result.links:
            print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
        print ('Gross Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,response.result.purchase_units[0].amount.value))
        return response
#     """This driver function invokes the get_order function with
#     order ID to retrieve sample order details. """
# if __name__ == '__main__':
#   GetOrder().get_order('REPLACE-WITH-VALID-ORDER-ID')


