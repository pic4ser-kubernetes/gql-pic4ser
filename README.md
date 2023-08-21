# GraphQL ROS PiC4Ser

## Description

This python package provides a mixin class for ROS nodes to send data to PiC4Ser Robot-UI GraphQL endpoints.

## Installation

```bash
pip install gql-pic4ser
```

## Usage

```python
from gql_pic4ser import GQLSendMixin

class MyNode(GQLSendMixin, Node):
    def __init__(self):
        super().__init__('http://localhost:4000/graphql', 'my_node')
        self.create_subscription(Int64, 'my_topic', self.callback_data, 10)

        self.create_subscription(String, 'my_topic_status', self.callback_status, 10)

        self.gql_add_webcam('session name', 'robot name', 'webcam name', 'http://192.168.127.84:8081/')

    def callback_data(self, msg: Int64):
        rt = self.get_clock().now().to_msg()
        dt = datetime.datetime.utcfromtimestamp(rt.sec)

        self.gql_add_data('session name', 'robot name', 'graph name', msg.data, dt.isoformat())

    def callback_status(self, msg: String):
        rt = self.get_clock().now().to_msg()
        dt = datetime.datetime.utcfromtimestamp(rt.sec)

        self.gql_update_status('session name', 'robot name', 'parameter name', msg.data, dt.isoformat())
```

A few things to note:

- The `GQLSendMixin` class requires to be subclassed before the Node class.
- When calling `super().__init__()` the first argument is the GraphQL endpoint URL.
- The type of message is String for status and any number (Int64 in this example) for data, it'll be converted to python float before sending the request.
- Both status and data need to be sent with a timestamp, in this case the timestamp is the ROS time converted to UTC.
