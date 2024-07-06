import time
import json
import gevent
from uuid import uuid4
from locust import events
import websocket
from proto.proto_tools import *


class SocketClient(object):
    def __init__(self, host):
        self.host = host
        self.session_id = uuid4().hex
        self.connect()

    def connect(self):
        self.ws = websocket.WebSocket()
        self.ws.settimeout(10)
        self.ws.connect(self.host)
        events.quitting.add_listener(self.on_close)
        self.attach_session()

    def attach_session(self):
        payload = {'action': 'attach_session', 'session_id': self.session_id}
        start_time = time.time()
        e = None
        try:
            response_message = self.send_with_response(proto_class=pb.AttachSession(), json_data=payload)
            data = json.loads(protobuf_to_json(response_message, pb.ServerResponse()))
            assert data.get('code') < 80
        except AssertionError as exp:
            e = exp
        except Exception as exp:
            e =exp
            self.ws.close()
            self.connect()
        elapsed = int((time.time() - start_time) * 1000)
        if e:
            events.request.fire(
                request_type='websocket', name='attach_session', response_time=elapsed, exception=e, response_length=len(json.dumps(data))
            )
        else:
            events.request.fire(
                request_type='websocket', name='attach_session', response_time=elapsed, response_length=len(json.dumps(data))
            )

    def send_with_response(self, proto_class, json_data):
        proto_data = message_to_protobuf(proto_class, json_data)
        g = gevent.spawn(self.ws.send, proto_data)
        g.get(block=True, timeout=2)
        g = gevent.spawn(self.ws.recv)
        result = g.get(block=True, timeout=10)
        return result
    def on_close(self):
        self.ws.close()

    def send(self, request_name, request_proto_class, response_proto_class, payload, assert_key, assert_info):
        message_id = uuid4().hex
        payload.update({'_messageId': message_id, 'session_id': self.session_id})
        start_time = time.time()
        e = None
        try:
            response_message = self.send_with_response(request_proto_class, payload)
            data = json.loads(protobuf_to_json(response_message, response_proto_class))
            # print(data)
            assert data.get(assert_key) < assert_info
        except AssertionError as exp:
            e = exp
        except Exception as exp:
            e = exp
            self.ws.close()
            self.connect()
        elapsed = int((time.time() - start_time) * 1000)
        if e:
            events.request.fire(
                request_type='websocket', name=request_name, response_time=elapsed, exception=e, response_length=len(json.dumps(data))
            )
        else:
            events.request.fire(
                request_type='websocket', name=request_name, response_time=elapsed, response_length=len(json.dumps(data))
            )

if __name__ == "__main__":
    import time

    # 修改为你的 WebSocket 服务地址
    ws_host = 'ws://localhost:6789'

    client = SocketClient(ws_host)

    # 测试发送和接收消息
    try:
        data = {
            "session_id": "123",
            "_messageId": "abc",
            "action": "do_something",
            "param": [
                {"param": "value"}
            ]
        }
        client.send('user_request', pb.UserRequest(),  pb.ServerResponse(), data, 'code', 95)
        print("Message sent successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # 等待一些时间以查看接收的消息
    time.sleep(5)