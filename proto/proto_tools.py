import json
from proto import message_pb2 as pb
from google.protobuf.json_format import ParseDict, MessageToJson


def json_to_protobuf(proto_class, json_data):
    # 创建一个 ClientRequest 实例
    proto_message = proto_class

    # 将 JSON 数据解析为 Protobuf 消息
    ParseDict(json_data, proto_message)

    return proto_message


def protobuf_to_json(serialized_message, proto_class):
    # 创建一个 MyMessage 实例
    proto_message = proto_class

    # 反序列化二进制字符串
    proto_message.ParseFromString(serialized_message)

    # 转换为 JSON 格式
    json_message = MessageToJson(proto_message)

    return json_message


def message_to_protobuf(proto_class, json_data):
    # 创建一个 MyMessage 实例
    proto_message = proto_class

    # 设置字段值
    proto_message = json_to_protobuf(proto_class, json_data)

    # 序列化为二进制字符串
    serialized_message = proto_message.SerializeToString()

    return serialized_message


def protobuf_to_message(proto_class, serialized_message):
    # 创建一个 MyMessage 实例
    proto_message = proto_class

    # 反序列化二进制字符串
    proto_message.ParseFromString(serialized_message)

    return proto_message


if __name__ == '__main__':
    # 示例 JSON 数据
    json_data = {
        "token": "123",
        "spath": "abc",
        "action": "do_something",
        "param": [
            {"param": "value1"}
        ]
    }

    # 将 JSON 转换为 Protobuf 消息
    protobuf_message = json_to_protobuf(pb.UserRequest(), json_data)
    serialized_message = message_to_protobuf(pb.UserRequest(), json_data)
    proto_message = protobuf_to_message(pb.UserRequest(), serialized_message)
    json_data = protobuf_to_json(serialized_message, pb.UserRequest())

    # print(protobuf_message)
    print(serialized_message)
    # print(proto_message)
    print(json_data)
