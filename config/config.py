import os

import yaml
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


def load_config():
    config_path = os.getenv("CONFIG_PATH", "config/config.yaml")

    logger.info(f"Carregando arquivo de configuração de {config_path}")

    try:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
            logger.info("Arquivo de configuração carregado com sucesso.")
    except FileNotFoundError as e:
        logger.error(f"Arquivo de configuração não encontrado: {e}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Erro ao analisar o arquivo de configuração: {e}")
        raise

    config["search_phrase"] = os.getenv(
        "SEARCH_PHRASE", config.get("search_phrase", "")
    )
    config["category"] = os.getenv("CATEGORY", config.get("category", ""))
    config["months"] = int(os.getenv("MONTHS", config.get("months", 6)))

    logger.debug(f"search_phrase configurado para: {config['search_phrase']}")
    logger.debug(f"category configurado para: {config['category']}")
    logger.debug(f"months configurado para: {config['months']}")

    return config
