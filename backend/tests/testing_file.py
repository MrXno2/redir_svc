from src.core.exception import UserNotFound
from src.core.logger import logger

class RRRTest:
    def func_test(self):
        logger.warning("отладка")


x = RRRTest()


x.func_test()

UserNotFound()