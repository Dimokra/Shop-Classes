import logging

logger = logging.getLogger("shop")
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("shop.log", encoding="utf-8")
fh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
logger.addHandler(fh)