import requests
import time
import pytest
from testcontainers.compose import DockerCompose
from pathlib import Path
from os import walk
from celery import states

PROJ_DIR = Path(__file__).resolve().parent.parent.parent
BASE_URL = "http://localhost"


@pytest.mark.slow
def test_upload_transaction():
    """
    Tests nginx, django, postgres, celery, rabbitmq
    """
    assert (True, "") == _is_proj_dir_set_properly()
    compose = _compose()
    with compose:

        celery_task_id = _upload_transactions_file()

        _ensure_celery_task_finished_successfuly(celery_task_id)

        _assert_transaction_correctly_processed()


def _is_proj_dir_set_properly():
    filenames = next(walk(PROJ_DIR), (None, None, []))[2]
    is_docker_compose_file_in_proj_path = (
        True if "docker-compose.yml" in filenames else False
    )
    if not is_docker_compose_file_in_proj_path:
        return (
            False,
            f"Improperly configured path to `docker-compose.yml`. Currently set to {PROJ_DIR=}",
        )
    return True, ""


def _compose() -> DockerCompose:
    return DockerCompose(
        PROJ_DIR,
        compose_file_name="docker-compose.yml",
        keep_volumes=True,
        pull=True,
        build=True,
    )


def _upload_transactions_file():
    url = f"{BASE_URL}/transactions/upload"
    file_path = PROJ_DIR / "tests" / "files" / "test.csv"
    with open(file_path, "rb") as f:
        file_bin = {"file": ("test.csv", f)}
        response = requests.post(url, files=file_bin)
        assert response.status_code == 200
        celery_task_id = response.json().get("celery_task_id")
        assert celery_task_id
    return celery_task_id


def _ensure_celery_task_finished_successfuly(celery_task_id, timeout=15):
    url = f"{BASE_URL}/transactions/processing-status/{celery_task_id}"
    for _ in range(timeout):
        r = requests.get(url)
        if r.status_code == 200 and r.json().get("task_status") == states.SUCCESS:
            return True
        time.sleep(1)
    raise Exception(
        f"Celery task {celery_task_id} did not finish in time {timeout=}. {r.status_code=} {r.json().get("task_status")=} {url=}"
    )


def _assert_transaction_correctly_processed():
    transaction_id = "d0466264-1384-4dc0-82d0-39e541b5c121"
    url = f"{BASE_URL}/transactions/{transaction_id}"
    response = requests.get(url)
    assert response.status_code == 200
    transaction_data = response.json()
    assert transaction_data == {
        "id": "d0466264-1384-4dc0-82d0-39e541b5c121",
        "timestamp": "2025-07-02T20:48:45.336874Z",
        "amount": "25.30",
        "currency": "PLN",
        "customer_id": "14245004-9354-4b77-8744-19e36372f4cd",
        "product_id": "0e64a915-9711-47f3-a640-be6f517546b1",
        "quantity": 5,
    }
