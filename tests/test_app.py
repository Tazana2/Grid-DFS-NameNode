from fastapi.testclient import TestClient
from main import app
from core.config import settings

client = TestClient(app)

def test_auth_and_register():
    # Login
    resp = client.post(f"{settings.API_V1_PREFIX}/auth/login", json={"username": "admin", "password": "admin123"})
    assert resp.status_code == 200
    token = resp.json()["access_token"]

    # Register datanode
    headers = {"Authorization": f"Bearer {token}"}
    dn = {"id": "dn1", "ip": "127.0.0.1", "port": 9000, "capacity": 1000}
    resp = client.post(f"{settings.API_V1_PREFIX}/namenode/register_datanode", json=dn, headers=headers)
    assert resp.status_code == 200

    # Allocate
    req = {"filename": "file.txt", "filesize": 128, "block_size": 64}
    resp = client.post(f"{settings.API_V1_PREFIX}/namenode/allocate", json=req, headers=headers)
    assert resp.status_code == 200
    assert "blocks" in resp.json()

    # Metadata
    resp = client.get(f"{settings.API_V1_PREFIX}/namenode/metadata/file.txt", headers=headers)
    assert resp.status_code == 200
