import json
import pytest
from app import app, socketio


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def socket_client():
    app.config["TESTING"] = True
    socketio_test = socketio.test_client(app)
    yield socketio_test
    socketio_test.disconnect()


class TestHealthEndpoint:
    def test_health_returns_ok(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "ok"

    def test_index_returns_html(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        assert b"AuraVision" in resp.data


class TestUpdateEndpoint:
    def test_update_with_valid_text(self, client):
        resp = client.post(
            "/update",
            data=json.dumps({"text": "hello world", "lang": "en"}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        assert resp.get_json()["success"] is True

    def test_update_missing_text(self, client):
        resp = client.post(
            "/update",
            data=json.dumps({"lang": "en"}),
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_update_empty_text(self, client):
        resp = client.post(
            "/update",
            data=json.dumps({"text": "   "}),
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_update_with_partial(self, client):
        resp = client.post(
            "/update",
            data=json.dumps({"text": "hel", "lang": "en", "partial": True}),
            content_type="application/json",
        )
        assert resp.status_code == 200

    def test_update_invalid_json(self, client):
        resp = client.post(
            "/update",
            data="not json",
            content_type="application/json",
        )
        assert resp.status_code == 400


class TestAuth:
    def test_update_without_token_when_required(self, client):
        import app as app_module
        original = app_module.AUTH_TOKEN
        app_module.AUTH_TOKEN = "test-secret"
        try:
            resp = client.post(
                "/update",
                data=json.dumps({"text": "hello"}),
                content_type="application/json",
            )
            assert resp.status_code == 401
        finally:
            app_module.AUTH_TOKEN = original

    def test_update_with_valid_token(self, client):
        import app as app_module
        original = app_module.AUTH_TOKEN
        app_module.AUTH_TOKEN = "test-secret"
        try:
            resp = client.post(
                "/update",
                data=json.dumps({"text": "hello"}),
                content_type="application/json",
                headers={"X-Auth-Token": "test-secret"},
            )
            assert resp.status_code == 200
        finally:
            app_module.AUTH_TOKEN = original

    def test_update_with_wrong_token(self, client):
        import app as app_module
        original = app_module.AUTH_TOKEN
        app_module.AUTH_TOKEN = "test-secret"
        try:
            resp = client.post(
                "/update",
                data=json.dumps({"text": "hello"}),
                content_type="application/json",
                headers={"X-Auth-Token": "wrong"},
            )
            assert resp.status_code == 401
        finally:
            app_module.AUTH_TOKEN = original


class TestConfig:
    def test_detect_lang_english(self):
        from config import detect_lang
        assert detect_lang("vosk-model-small-en-us-0.15") == "en"
        assert detect_lang("english-model") == "en"

    def test_detect_lang_farsi(self):
        from config import detect_lang
        assert detect_lang("vosk-model-small-fa-0.5") == "fa"
        assert detect_lang("farsi-model") == "fa"

    def test_detect_lang_spanish(self):
        from config import detect_lang
        assert detect_lang("vosk-model-small-es-0.42") == "es"
        assert detect_lang("spanish-model") == "es"

    def test_detect_lang_unknown(self):
        from config import detect_lang
        assert detect_lang("some-random-model") == "unknown"
