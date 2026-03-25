from fastapi.testclient import TestClient
from fastapi import status

from app.models import FocusStep


class TestCreateFocusSession:
  def test_create_session_success(self, client: TestClient, auth_headers, test_focus_step: FocusStep):
    res = client.post(f"/focus_step/{test_focus_step.id}")
    assert res.status_code == status.HTTP_201_CREATED