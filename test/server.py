import asyncio
import json
import websockets
from proto.proto_tools import *
import random

# WebSocket 服务器
connected_clients = set()

async def websocket_handler(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            try:
                data = json.loads(protobuf_to_json(message.encode(), pb.UserRequest()))
            except:
                data = json.loads(protobuf_to_json(message.encode(), pb.AttachSession()))

            # print(data)
            response = {
                'code': random.randint(0,100),
                'msg': 'request success',
                'data': [
                    {"data": data.get('action')}
                ]
            }
            response_data = message_to_protobuf(proto_class=pb.ServerResponse(), json_data=response)
            await websocket.send(response_data)
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")
    finally:
        connected_clients.remove(websocket)

if __name__ == '__main__':
    # 启动 WebSocket 服务器
    start_server = websockets.serve(websocket_handler, "0.0.0.0", 6789)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()