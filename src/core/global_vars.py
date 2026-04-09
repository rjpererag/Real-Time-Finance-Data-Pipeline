import os
from dataclasses import dataclass


@dataclass(frozen=True)
class GlobalVars:
    topic_name: str = "my-finance-pipeline"
    kafka_bootstrap_server: str = os.getenv("KAFKA_BOOTSTRAP_SERVER", "localhost:29092")
    kafka_group_id: str = os.getenv("KAFKA_GROUP_ID", "localhost:29092")
    postgres_db: str = os.getenv("POSTGRES_DB", "my_postgres")
    postgres_user: str = os.getenv("POSTGRES_USER", "postgres")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "admin")
    postgres_port: str = os.getenv("POSTGRES_PORT", 5432)
    postgres_url: str = os.getenv("POSTGRES_URL", "jdbc:postgresql://localhost:5432/my_postgres")


global_vars = GlobalVars()
