from logs.core.factory import LogFactory

logger = LogFactory.create_logger(__name__)
print(logger.get_all_issues())

logger.info("INFO.")

if __debug__:
    logger.debug("DEBUG.")

logger.warning("WARNING.")
logger.error("ERROR.")
logger.critical("CRITICAL.")

logger.error("DUMMY ERROR.", extra={"issue": "MyCustomWarning"})
