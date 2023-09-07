from botbuilder.core import TurnContext
from botbuilder.core.bot import Bot

class MyBot(Bot):

    async def on_turn(self, turn_context: TurnContext):
        # Check for message activity type
        if turn_context.activity.type == "message":
            # Send a fixed message
            await turn_context.send_activity("Hello from the bot!")
        else:
            await super().on_turn(turn_context)
