from pydantic import BaseSettings


class CoreSettings(BaseSettings):
    gcp_project_id: str

    class Config:
        env_file = ".env"