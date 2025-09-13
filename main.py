from time import sleep
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_openai import ChatOpenAI

from chat_history import ChatHistory
from chatbot_api import Chatbot
from mqtt_connect import MQTT_Connection


if __name__ == "__main__":
    print("Starting MQTT Chatbot...", flush=True)

    chat_history = ChatHistory()
    print("Chat history initialized.", flush=True)

    chatbot = None

    # try:
    #     model = ChatOpenAI(
    #         model="qwen/qwen3-30b-a3b-2507",
    #         openai_api_key="not-needed",
    #         openai_api_base="http://192.168.1.1:1234/v1"
    #     )
    #     print("Testing Qwen-3-30B-A3B-2507 model...", flush=True)
    #     model.invoke("")
    #     chatbot = Chatbot(model)
    #     print("Using Qwen-3-30B-A3B-2507 model", flush=True)
    # except Exception as _:
    #     print("Qwen-3-30B-A3B-2507 model not available", flush=True)
    
    if not chatbot:
        try:
            with open("./api_key.txt") as file:
                api_key = file.read().strip()
            model = ChatMistralAI(
                model="mistral-medium-latest",
                api_key=api_key
            )
            print("Testing Mistral-Medium-Latest model...", flush=True)
            # model.invoke("")
            chatbot = Chatbot(model)
            print("Using Mistral-Medium-Latest model", flush=True)
        except Exception as _:
            print("Mistral-Medium-Latest model not available", flush=True)

    if not chatbot:
        print("No model available, exiting...", flush=True)
        exit(1)

    def on_new_message(conn: MQTT_Connection, chat: ChatHistory):
        response = chatbot.chat(chat)
        if response:
            conn.publish(response)

    mqtt_connection = MQTT_Connection(chat_history, on_new_message)