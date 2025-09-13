from chat_history import ChatHistory
import paho.mqtt.client as mqtt

class MQTT_Connection:

    def __init__(self,
        chat: ChatHistory,
        on_message:  callable,
        address: str = "test.mosquitto.org",
        topic:   str = "irco"
    ):
        self.__chat = chat
        self.__on_message = on_message
        self.__address = address
        self.__base_topic = topic

        self.__client = mqtt.Client()
        self.__client.connect(self.__address)
        
        self.__listen()

    def publish(self,
        message: str,
        name:    str = "chatbot"
    ):
        self.__client.publish(f"{self.__base_topic}/{name}", message)
        self.__chat.add_message("assistant", name, message)

    def __listen(self):
        def __on_message(client, userdata, message):
            name = message.topic.split("/")[-1]
            payload = message.payload.decode()

            if (
                len(self.__chat.get_chat()) == 0 or
                self.__chat.get_chat()[-1].role() != "assistant" or
                payload != self.__chat.get_chat()[-1].message()
            ):
                self.__chat.add_message("user", name, payload)
                self.__on_message(self, self.__chat)

        self.__client.subscribe(f"{self.__base_topic}/+")
        self.__client.on_message = __on_message
        print("MQTT: Listening for messages...", flush=True)
        self.__client.loop_forever()