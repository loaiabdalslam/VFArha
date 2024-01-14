from telegram import Update
import google.generativeai as genai

import logging
from collections import defaultdict
from typing import DefaultDict, Optional, Set

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ExtBot,
    TypeHandler,
    ApplicationBuilder,
    MessageHandler,
    filters
)





BOT_TOKEN='6916124264:AAFYyT3FB2Tv8iLUfqFxvvkU2sfCKtLPJS8'
BOT = '@vFarhaTherapyBot'
GEMENI_PRO = 'AIzaSyA0rakuiHOUDkIlP6Nm_-O182KPaoEm9eI'

genai.configure(api_key=GEMENI_PRO)
model = genai.GenerativeModel(model_name = "gemini-pro")




# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)



class ChatData:
    """Custom class for chat_data. Here we store data per message."""

    def __init__(self) -> None:
        self.messages: DefaultDict[str,str] = defaultdict(str)


# The [ExtBot, dict, ChatData, dict] is for type checkers like mypy
class CustomContext(CallbackContext[ExtBot, dict, ChatData, dict]):
    """Custom class for context."""

    def __init__(
        self,
        application: Application,
        chat_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ):
        super().__init__(application=application, chat_id=chat_id, user_id=user_id)
        self._message_id: Optional[int] = None

    @property
    def bot_user_ids(self) -> Set[int]:
        """Custom shortcut to access a value stored in the bot_data dict"""
        return self.bot_data.setdefault("user_ids", set())

    @property
    def messages(self) -> Optional[str]:
        """Access the number of clicks for the message this context object was built for."""
        if self._message_id:
            return self.chat_data.messages[self._message_id]
        return None

    @messages.setter
    def messages_adding(self, value: int) -> None:
        """Allow to change the count"""
        if not self._message_id:
            raise RuntimeError("There is no message associated with this context object.")
        self.chat_data.messages[self._message_id] = value



    @classmethod
    def from_update(cls, update: object, application: "Application") -> "CustomContext":
        """Override from_update to set _message_id."""
        # Make sure to call super()
        context = super().from_update(update, application)

        if context.chat_data and isinstance(update, Update) and update.effective_message:
            # pylint: disable=protected-access
            context._message_id = update.effective_message.message_id

        # Remember to return the object
        return context


# Function to start the bot
async def start(update: Update, context: CustomContext) -> None:
    await update.message.reply_text('انا فرحة وهنبدأ مع بعض السيشن اللطيفة الي هتطلع منها بنصائح ايجابية لحالتك النفسية ، حاول تكتب كل حاجة حاسس بيها في رسالة واحدة والرد  ممكن هيتأخر شوية بس ان شاء الله يكون هو الرد الي انت محتاجه  ')

# Function to handle incoming messages
async def handle_message(update: Update, context: CustomContext) -> None:
    user_id = update.message.from_user.id
    user_message = update.message.text

    # Get the existing user context or create a new one


    # Process the message using Gemini API (replace with your actual Gemini API calls)
    gemini_response = await process_gemini_api(user_message)

    # Respond to the user
    await update.message.reply_text(gemini_response)

# Function to process Gemini API (replace with your actual Gemini API logic)
async def process_gemini_api(user_context):
    # Add your Gemini API logic here
    # Use GEMINI_API_KEY and GEMINI_API_SECRET for authentication
    # Access user context, e.g., user_message = user_context.get('message', '')

    # For demonstration purposes, we'll just return a dummy response

    prompt_parts = [f"You are an Egyptian psychiatrist  its name is فرحة. All your responses are in the Egyptian dialect. The context will be based on all of these messages {user_context}",
     "You  will analyze the context and give direct, effective psychological advice based on the previous context.",
       "If the words are outside the context of the psychological complaint, you will respond by saying: I apologize, I don’t understand very much what you are saying"
    ]
    response =  model.generate_content(prompt_parts)
    
    print(response.text)

    return response.text

def main() -> None:
        
        context_types = ContextTypes(context=CustomContext, chat_data=ChatData)

        application = ApplicationBuilder().token(BOT_TOKEN).context_types(context_types).build()

        incoming_message_handler = MessageHandler(filters.TEXT,handle_message)

        start_handler = CommandHandler(
            'start',
             start
        )


        application.add_handler(start_handler)
        application.add_handler(incoming_message_handler)

        application.run_polling(poll_interval=3,allowed_updates=Update.ALL_TYPES)




if __name__ == '__main__':
        main()

