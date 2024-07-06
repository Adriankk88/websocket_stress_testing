from locust import User, TaskSet, task
from client.socket_client import SocketClient
from proto.proto_tools import *

class WSBehavior(TaskSet):
    @task
    def action(self):
        data = {
        "session_id": "session_id",
        "_messageId": "_messageId",
        "action": "do_something_right",
        "param": [
            {"param": "value"}
        ]
        }
        self.client.send('user_request', pb.UserRequest(),  pb.ServerResponse(), data, 'code', 95)


    @task
    def action2(self):
        data = {
            "session_id": "session_id",
            "_messageId": "_messageId",
            "action": "do_something_right",
            "param": [
                {"param": "value"}
            ]
        }
        self.client.send('user_request', pb.UserRequest(),  pb.ServerResponse(), data, 'code', 95)

class WSUser(User):
    tasks = [WSBehavior]
    min_wait = 1000
    max_wait = 3000

    def __init__(self, *args, **kwargs):
        super(WSUser, self).__init__(*args, **kwargs)
        self.client = SocketClient(self.host)

