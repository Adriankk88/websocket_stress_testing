from locust import HttpUser, User, task
from tasks.websocket_tasks import WSUser

class MyTest(WSUser):
    pass