import os
from pydantic_settings import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = os.path.join(BASE_DIR, ".env")

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    DATABASE_URL: str
    DATABASE_HOST_OVERRIDE: str | None = None
    AUTO_CREATE_TABLES: bool = False
    DEVICE_CONTROL_KEY: str | None = None
    DEVICE_CONTROL_KEYS: str | None = None
    DEVICE_PROVISIONING_KEY: str | None = None
    COMMAND_ACK_TIMEOUT_SECONDS: int = 3
    COMMAND_RESULT_TIMEOUT_SECONDS: int = 10
    BOARD_HEARTBEAT_STALE_SECONDS: int = 15
    AUDIO_TRANSCRIPTION_MODEL: str = "small"
    AUDIO_TRANSCRIPTION_DEVICE: str = "cpu"
    AUDIO_TRANSCRIPTION_COMPUTE_TYPE: str = "int8"
    AUDIO_TRANSCRIPTION_BEAM_SIZE: int = 3
    AUDIO_TRANSCRIPTION_VAD_FILTER: bool = True
    AUDIO_TRANSCRIPTION_INITIAL_PROMPT: str = (
        "스마트 제조 장비 제어 명령입니다. 장비명은 기본 컨베이어, 컨베이어, "
        "색상분류 컨베이어, 피더, AGV입니다. 명령은 상태 확인, 시작, 정지, "
        "비상 정지, 속도 변경, 정방향, 역방향, 색상 설정, 복귀, 적재함입니다."
    )

    model_config = {
        "env_file": ENV_PATH,
        "env_file_encoding": "utf-8"
    }

settings = Settings()
