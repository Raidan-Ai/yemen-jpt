from yemenjpt.config.settings import Settings


def test_settings_defaults() -> None:
    settings = Settings()
    assert settings.APP_HOST == "0.0.0.0"
    assert settings.APP_PORT == 8000