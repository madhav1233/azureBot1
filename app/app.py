from flask import Flask, request, jsonify
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from bot.mybot import MyBot
import os
import logging

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
    if "application/json" in request.headers["Content-Type"]:
        body = request.json
    else:
        return jsonify({"error": "Expecting application/json in request header's Content-Type."}), 400

    async def call_bot_framework():
        activity = TurnContext.apply_conversation_reference(body, BotFrameworkAdapter.get_conversation_reference(body))
        await ADAPTER.process_activity(activity, BOT.on_turn)

    loop.run_until_complete(call_bot_framework())
    return jsonify({"status": "Message processed"}), 200

if __name__ == "__main__":
    app.run(port=3978)
