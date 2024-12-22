import os

class Config:
    """Configuration class for environment variables and constants."""

    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/tmp/output")
    LOGS_DIR = os.getenv("LOGS_DIR", "/tmp/logs")
    USERNAME = os.getenv("USERNAME", "default_user")
    PASSWORD = os.getenv("PASSWORD", "default_password")

    # Define dynamic environments with their corresponding catalog, space, and org values
    ENVIRONMENTS = {
        "dev": {
            "catalog": "central",
            "space": "cs1",
            "org": "api_dev",
        },
        "sit1": {
            "catalog": "enterprise",
            "space": "cs2",
            "org": "api_sit1",
        },
        "sit2": {
            "catalog": "central",
            "space": "cs3",
            "org": "api_sit2",
        },
        "prod": {
            "catalog": "enterprise",
            "space": "cs4",
            "org": "api_prod",
        },
    }

    # Default fallback values (if an env key is missing)
    DEFAULT_ENV = "dev"

    @classmethod
    def get_config_for_env(cls, env):
        """Fetch configuration for the given environment."""
        return cls.ENVIRONMENTS.get(env, cls.ENVIRONMENTS[cls.DEFAULT_ENV])
