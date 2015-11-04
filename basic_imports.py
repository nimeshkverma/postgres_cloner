import logging
LOGGER = logging.getLogger("search_relevance_app")

logging.basicConfig(filename="db_split.log", level=logging.INFO,
                    format='%(asctime)s.%(msecs)d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
