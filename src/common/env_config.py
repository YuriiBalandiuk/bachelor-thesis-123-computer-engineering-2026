import os
import logging

from typing import Optional
from dotenv import load_dotenv


logger = logging.getLogger(__name__)


class EnvConfigError(Exception):
    """
    Raised when environment configuration is invalid or incomplete.

    This exception indicates that one or more required environment
    variables are missing, empty, or improperly defined.
    """

class EnvConfig():
    """
    Provide validated access to environment configuration variables.

    The class loads environment variables from a '.env' file once per
    process lifecycle and enforces the presence of required keys.
    Access to configuration values is exposed through strongly-defined
    properties.

    Attributes:
        _is_loaded (bool): Class-level flag indicating whether the
            environment has already been loaded.
    """
    _is_loaded = False


    def __init__(self,  
        env_path: str = ".env", 
        required_keys: Optional[list[str]] = None
    ):
        """
        Initialize environment configuration.

        Loads environment variables from the specified file and validates
        required keys if provided.

        Args:
            env_path: Path to the '.env' file.
            required_keys: Optional list of environment variable names
                that must be present.

        Raises:
            FileNotFoundError: If the environment file cannot be loaded.
            EnvConfigError: If any required key is missing.
        """
        load_dotenv(env_path)
        
        if not EnvConfig._is_loaded:
            EnvConfig._is_loaded = True
            if not EnvConfig._is_loaded:
                raise FileNotFoundError(f"Failed load {env_path}")


        if required_keys:
            missing = [key for key in required_keys if os.getenv(key) is None]
            if missing:
                raise EnvConfigError(f"Required keys are missing: {', '.join(missing)}")


    def _get(self, 
        key: str
    ) -> str:
        """
        Retrieve a required environment variable.

        Args:
            key: Name of the environment variable.

        Returns:
            The value associated with the given key.

        Raises:
            EnvConfigError: If the variable is missing or empty.
        """
        value = os.getenv(key)
        if not value:
            raise EnvConfigError(f"Required key are missing in '.env' - {key}")
        return value


    def _build_topics(self, 
        env_keys: str
    ) -> list[str]:
        """
        Build MQTT subscription topics from environment variable.

        The specified environment variable must contain a comma-separated
        list of channel identifiers. Each identifier is transformed into
        a subscription topic using the pattern:
        'channels/<channel_id>/subscribe'.

        Args:
            env_keys: Name of the environment variable containing
                comma-separated channel identifiers.

        Returns:
            List of formatted MQTT subscription topics.

        Raises:
            EnvConfigError: If the environment variable is missing,
                empty, or contains invalid channel identifiers.
        """
        list_env_keys = [i.strip() for i in self._get(env_keys).split(',')]
        logger.info(list_env_keys)
        
        topics = []
        for key in list_env_keys:
            if not key:
                raise EnvConfigError(f"Required key are missing in '.env' file - {key}")
            topics.append(f"channels/{key}/subscribe")
        return topics


    @property
    def client_id(self) -> str:
        """
        Return MQTT client identifier.

        Returns:
            The value of the 'CLIENT_ID' environment variable.

        Raises:
            EnvConfigError: If the variable is missing or empty.
        """
        return self._get("CLIENT_ID")


    @property
    def mqtt_username(self) -> str:
        """
        Return MQTT authentication username.

        Returns:
            The value of the 'MQTT_USERNAME' environment variable.

        Raises:
            EnvConfigError: If the variable is missing or empty.
        """
        return self._get("MQTT_USERNAME")


    @property
    def mqtt_password(self) -> str:
        """
        Return MQTT authentication password.

        Returns:
            The value of the 'MQTT_PASSWORD' environment variable.

        Raises:
            EnvConfigError: If the variable is missing or empty.
        """
        return self._get("MQTT_PASSWORD")
    

    @property
    def mqtt_channels(self) -> list[str]:
        """
        Return formatted MQTT subscription topics.

        The topics are derived from the 'CHANNEL_IDS' environment
        variable.

        Returns:
            List of MQTT subscription topic strings.

        Raises:
            EnvConfigError: If 'CHANNEL_IDS' is missing, empty,
                or contains invalid values.
        """
        return self._build_topics("CHANNEL_IDS")
    

    @property
    def superset_key(self) -> str:
        """
        Return Superset integration key.

        Returns:
            The value of the 'SUPERSET_KEY' environment variable.

        Raises:
            EnvConfigError: If the variable is missing or empty.
        """
        return self._get("SUPERSET_KEY")


    @property
    def iceberg_warehouse_catalog(self) -> str:
        """
        Return iceberg warehouse catalog integration path.

        Returns:
            The value of the 'ICEBERG_WAREHOUSE_CATALOG' environment variable.

        Raises:
            EnvConfigError: If the variable is missing or empty.
        """
        return self._get("ICEBERG_WAREHOUSE_CATALOG")


    @property
    def iceberg_db(self) -> str:
        """
        Return iceberg database integration key.

        Returns:
            The value of the 'ICEBERG_DB' environment variable.

        Raises:
            EnvConfigError: If the variable is missing or empty.
        """
        return self._get("ICEBERG_DB")


    @property
    def iceberg_table(self) -> str:
        """
        Return iceberg table integration key.

        Returns:
            The value of the 'ICEBERG_TABLE' environment variable.

        Raises:
            EnvConfigError: If the variable is missing or empty.
        """
        return self._get("ICEBERG_TABLE")
    

    @property
    def iceberg_table_path(self) -> str:
        """
        Return iceberg table integration path.

        Returns:
            The value of the 'ICEBERG_TABLE_PATH' environment variable.

        Raises:
            EnvConfigError: If the variable is missing or empty.
        """
        return self._get("ICEBERG_TABLE_PATH")


    @property
    def iceberg_checkpointlocation_path(self) -> str:
        """
        return iceberg checkpointlocation integration path.

        Returns:
            The value of the 'ICEBERG_CHECKPOINTLOCATION_PATH' environment variable.

        Raises:
            EnvConfigError: If the variable is missing or empty.
        """
        return self._get("ICEBERG_CHECKPOINTLOCATION_PATH")