from time import localtime, strftime, time_ns


class ChatHistory:

    TIMEOUT = 5  # minutes
    MIN_MESSAGES = 20

    class __ChatMessage:

        def __init__(self,
            role: str,
            name: str,
            message: str
        ):
            self.__role: str = role
            self.__name: str = name
            self.__message: str = message
            self.__timestamp: int = time_ns()

        def role(self) -> str:
            return self.__role
    
        def name(self) -> str:
            return self.__name
        
        def message(self) -> str:
            return self.__message
        
        def timestamp(self) -> int:
            return self.__timestamp


    def __init__(self):
        self.__chat: list[ChatHistory.__ChatMessage] = []
        self.__users: set[str] = set()
    
    def add_message(self,
        role: str,
        name: str,
        message: str
    ):
        # Remove old messages
        self.__chat = [
            msg
            for msg in self.__chat[:-ChatHistory.MIN_MESSAGES]
            if (time_ns() - msg.timestamp()) < ChatHistory.TIMEOUT * 60 * 1_000_000_000
        ] + self.__chat[-ChatHistory.MIN_MESSAGES:]
        
        # Remove 'disconnected' users
        self.__users = {
            msg.name()
            for msg in self.__chat
            if msg.role() == "user"
        }

        if role == "user":
            # Register new user
            if name not in self.__users:
                self.__chat.append(ChatHistory.__ChatMessage("system", "", f"User '{name}' joined the chat."))
                self.__users.add(name)
                print(f"[{strftime('%H:%M:%S', localtime())}] User '{name}' joined the chat.", end="", flush=True)

        # Add message to chat history
        self.__chat.append(ChatHistory.__ChatMessage(role, name, message))
        print(f"[{strftime('%H:%M:%S', localtime())}] <{name}>  {message}", end="", flush=True)
    
    def get_chat(self) -> list[__ChatMessage]:
        return self.__chat