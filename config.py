from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    bind_host: str = "0.0.0.0"
    bind_port: int = 8000

    database_user: str
    database_password: str
    database_host: str = "localhost"
    database_port: int = 3306
    database_name: str

    yolov5_deepsort_interpreter: str
    yolov5_deepsort_path: str
    yolov5_deepsort_main: str = "main.py"
    yolov5_deepsort_result_json: str = "count_result.json"
    yolov5_deepsort_result_video: str = "result_video.mp4"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Config()
