import atexit
import logging
import logging.config
from pathlib import Path
from typing import ClassVar

import yaml

import logs.issues  # noqa: F401
from logs.core.adapter import IssueRegistryAdapter


class LogFactory:
    """
    Factory class for setting up logging configurations.
    Adheres to SRP by focusing solely on logger setup.
    Uses Lazy Loading DP for singleton initialization.
    """

    DEFAULT_CONFIG_PATH: ClassVar[str | Path] = (
        Path(__file__).parent.parent / "settings/config.yaml"
    )
    _initialized: ClassVar[bool] = False

    @classmethod
    def _initialize(cls) -> None:
        """
        Ensures logging is setup only once
        """
        if not cls._initialized:
            cls._setup_logging()
            cls._start_queue_listener()
            cls._initialized = True

    @classmethod
    def _setup_logging(cls, config_path: Path | str | None = None) -> None:
        """
        Private method to set up logging using the configuration file.
        """
        config_path = Path(config_path) if config_path else cls.DEFAULT_CONFIG_PATH

        try:
            with open(config_path, "r") as file:
                config = yaml.safe_load(file)
                logging.config.dictConfig(config)  # type: ignore

        except (FileNotFoundError, yaml.YAMLError):
            # Fall back to some default logger config
            logging.basicConfig(level=logging.INFO)
            logging.warning("Falling back to default logging config...")

        except Exception as e:
            raise RuntimeError(f"Unexpected error setting up logging: {e}")

    @classmethod
    def _start_queue_listener(cls) -> None:
        """
        Initialize queues.
        """
        queue_handler = logging.getHandlerByName("queueHandler")
        if queue_handler:
            queue_handler.listener.start()  # type: ignore
            atexit.register(queue_handler.listener.stop)  # type:ignore

    @classmethod
    def create_logger(cls, name: str) -> IssueRegistryAdapter:
        """
        Static method to retrieve a logger by name.

        Args:
            name (str): Name of the logger

        Returns:
            logging.Logger: Logger instance
        """
        cls._initialize()  # Ensure logging is set up before returning a logger
        logger = IssueRegistryAdapter(logging.getLogger(name), {})

        return logger


if __name__ == "__main__":
    logger = LogFactory.create_logger(__name__)
    print(logger.get_all_issues())

    logger.info("INFO.")

    if __debug__:
        logger.debug("DEBUG.")

    logger.warning("WARNING.")
    logger.error("ERROR.")
    logger.critical("CRITICAL.")

    logger.error("DUMMY ERROR.", extra={"issue": "MyCustomWarning"})
