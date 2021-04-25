from pydantic import BaseSettings


class CoreSettings(BaseSettings):
    # 変数が不要な場合ようにダミーの文字列を設定
    gcp_project_id: str = "xxx"

    class Config:
        env_file = ".env"