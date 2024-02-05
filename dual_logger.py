
from aiologger import Logger
from aiologger.handlers.streams import AsyncStreamHandler
from aiologger.handlers.files import AsyncFileHandler

class DualLogger:
    def __init__(self, log_file_path, log_to_console=True, log_to_file=True):
        self.logger = Logger.with_default_handlers()

        if log_to_console:
            # Додати обробник для виведення в консоль
            console_handler = AsyncStreamHandler()
            self.logger.add_handler(console_handler)

        if log_to_file:
            # Додати асинхронний обробник для запису у файл
            file_handler = AsyncFileHandler(log_file_path)
            self.logger.add_handler(file_handler)



# Приклад використання:
if  __name__ == "__main__":
    logger = DualLogger("server_log.txt", log_to_console=True, log_to_file=True).logger
    logger.info("Це повідомлення буде виведено і в консоль, і в файл.")
    