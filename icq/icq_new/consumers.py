from channels.consumer import AsyncConsumer
from icq_new.ai import *


class YourConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        await self.send({"type": "websocket.accept"})

    async def websocket_receive(self, text_data):
        for key in text_data:
            print("key: ", key)
        text = text_data.get("text").replace('{"message":"', "").replace('"}',"")
        answer = get_answer(text)
        await self.send({
            "type": "websocket.send",
            "text": answer
        })

    async def websocket_disconnect(self, event):
        pass