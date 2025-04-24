import logging

class _Logger:
    _instance = None

    @staticmethod
    def get():
        if _Logger._instance is None:
            _Logger()
        return _Logger._instance

    def __init__(self):
        if _Logger._instance is not None:
            raise Exception("Logger is a singleton!")
        self.logger = logging.getLogger("pattern_miner")
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s %(levelname)s — %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        _Logger._instance = self.logger
