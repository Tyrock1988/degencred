import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("logs/bot.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def detect_payment(message):
    logger.debug("Processing message: %s", message)
    try:
        if not message:
            logger.warning("Empty message received")
            return None
        logger.info("Detected payment: %s", message)
        return {"user": "user123", "amount": 5}
    except Exception as e:
        logger.error("Payment detection error: %s", e)
        return None
