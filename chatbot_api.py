from typing import Optional
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

from chat_history import ChatHistory

class Chatbot:

    class __ChatResponse(BaseModel):
        message: Optional[str] = None

    def __init__(self,
        model: any,
    ):
        self.__model = model
    
    def chat(self,
        chat_history: ChatHistory,
    ) -> str:
        context = "You are a chatbot that helps making a chat more lively. " + \
                  "You must try (while not forcing if they don't want) to engage in conversations with the peoples here.\n" + \
                  "You will sometimes see users joining the chat. You must try to engage them in conversation.\n" + \
                  "Most peoples use this chat to test their MQTT connection, so beware that somme message, especially the first message after joining, may be hard to understand. " + \
                  "In these cases, just pretend they hadn't wrote anything, and, if they just joined the chat, try to welcome them. "\
                  "However, since everyone knows this chat is usually used for this purpose, there's no need to explain this to everyone.\n" + \
                  "If multiple users are present, try to include them all in the conversation. " + \
                  "If users talks to each other, don't interrupt them if it's not relevant, for example if they ask a question to each other. " + \
                  "Also, a good idea can be to give the subject and even a quick summary of the conversation so far to new users, but only if there was a conversation before. If not, try to start one from scratch.\n" + \
                  "If it looks like you've forgotten something, don't hesitate to ask the users again.\n" + \
                  "You can use long or medium size messages, depending on the context.\n"
        prompt_messages = [
            ("system", context),
        ]

        for chat_message in chat_history.get_chat():
            if chat_message.role() == "assistant":
                prompt_messages.append(("assistant", chat_message.message()))
            elif chat_message.role() == "user":
                prompt_messages.append(("user", f"[User '{chat_message.name()}']: {chat_message.message()}"))
            else:
                prompt_messages.append(("user", f"[System]: {chat_message.message()}"))

        prompt_template = ChatPromptTemplate.from_messages(prompt_messages)
        chain = prompt_template | self.__model.with_structured_output(schema=Chatbot.__ChatResponse)
        return chain.invoke({"input": ""}).message