import logging

class Logger:
    """
        This class it will responsable for logs manipulations and settings
    """

    def __init__(self, module:str = __name__):
        self.logger = logging.getLogger(module)
 
    #@staticmethod
    def emit(self, message:str, category:str = 'INFO'):
        # Define a particular log format
        log_format = "[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s"
        #formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")

        logging.basicConfig(level=logging.INFO, format=log_format, datefmt="%Y-%m-%d %H:%M:%S")
        
        # Separe output messages, due a log category
        try:
            if category == 'INFO':
                self.logger.info(message)
            elif category == 'DEBUG':
                self.logger.debug(message)
            elif category == 'WARNING':
                self.logger.warning(message)
            elif category == 'CRITICAL':
                self.logger.warning(message)
            elif category == 'ERROR':
                self.logger.error(message)
        except Exception as e:
            raise ValueError(f'We have found the following error when trying to set logger category type: {e}')
        