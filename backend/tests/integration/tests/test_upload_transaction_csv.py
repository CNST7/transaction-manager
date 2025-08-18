import time
from os import walk
from pathlib import Path

import pytest
import requests
from testcontainers.compose import DockerCompose
from transactionManagerProcessor.enums import ProcessingStatus

PROJ_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
BASE_URL = "http://localhost"


@pytest.mark.integration
def test_upload_transaction_csv():
    """
    Test stack: nginx, django, rabbitmq, celery, postgresql
    """
    if not _is_proj_directory_set_properly():
        raise Exception(
            f"Improperly configured path to `docker-compose.yml`. Currently set to {PROJ_DIR=}"
        )
    compose = _build_project()
    with compose:
        transaction_csv_id = _upload_csv()
        _ensure_celery_task_finished_successfuly(transaction_csv_id)
        _assert_transaction_correctly_processed()


def _is_proj_directory_set_properly():
    filenames = next(walk(PROJ_DIR), (None, None, []))[2]
    is_docker_compose_file_in_proj_path = (
        True if "docker-compose.yml" in filenames else False
    )
    if not is_docker_compose_file_in_proj_path:
        return False
    return True


def _build_project() -> DockerCompose:
    return DockerCompose(
        PROJ_DIR,
        compose_file_name=("docker-compose.yml", "docker-compose.test.yml"),
        pull=True,
        build=True,
        keep_volumes=True,
        env_file=".env",
    )


def _upload_csv():
    url = f"{BASE_URL}/transactions/upload"
    transaction_csv_path = (
        PROJ_DIR / "backend" / "tests" / "integration" / "fixtures" / "test.csv"
    )
    with open(transaction_csv_path, "rb") as f:
        file_bin = {"file": ("test.csv", f)}
        response = requests.post(url, files=file_bin)
        transaction_csv_id = response.json().get("transaction_csv_id")
        assert response.status_code == 200
        assert transaction_csv_id
    return transaction_csv_id


_statuses_indicating_finished_processing = (
    ProcessingStatus.SUCCESS,
    ProcessingStatus.FAIL,
)


def _ensure_celery_task_finished_successfuly(transaction_csv_id, timeout=15):
    url = f"{BASE_URL}/transactions/processing-status/{transaction_csv_id}"
    for _ in range(timeout):
        r = requests.get(url)
        processing_status = ProcessingStatus(r.json().get("status"))
        if (
            r.status_code == 200
            and processing_status in _statuses_indicating_finished_processing
        ):
            return True
        time.sleep(1)
    raise Exception(
        f"Process transaction csv timeout after {timeout=}. {transaction_csv_id=} {r.status_code=} {processing_status=} {url=}"
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
