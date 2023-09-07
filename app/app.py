from flask import Flask, request, jsonify
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity
from bot.mybot import MyBot
import os
import logging
import asyncio


app = Flask(__name__)

MICROSOFT_APP_ID = os.environ.get("MICROSOFT_APP_ID")
MICROSOFT_APP_PASSWORD = os.environ.get("MICROSOFT_APP_PASSWORD")

# Set up the BotFrameworkAdapter
SETTINGS = BotFrameworkAdapterSettings(MICROSOFT_APP_ID, MICROSOFT_APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)
BOT = MyBot()

logging.basicConfig(level=logging.INFO)

@app.route("/api/messages", methods=["POST"])
def messages():
    print("Headers:", request.headers)
    print("Body:", request.data)
    if "application/json" in request.headers["Content-Type"]:
        body = request.json
        print(body)
        
        activity = Activity.deserialize(body)
        activity.service_url = body.get("service_url")
        conversation_reference = TurnContext.get_conversation_reference(activity)
        activity = TurnContext.apply_conversation_reference(activity, conversation_reference)
        
        async def call_bot_framework():
            try:
                await ADAPTER.process_activity(activity, "", BOT.on_turn)
            except Exception as exception:
                print("Error:", str(exception))
                raise

        loop = asyncio.get_event_loop()
        loop.run_until_complete(call_bot_framework())
        return jsonify({"status": "Message processed"}), 200
    else:
        return jsonify({"error": "Expecting application/json in request header's Content-Type."}), 400


if __name__ == "__main__":
    app.run(port=3978)
