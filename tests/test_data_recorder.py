import csv

import pytest

from engine.data_recorder import CSV_HEADER, ensure_data_file, save_training_row


def test_ensure_data_file_creates_file(tmp_path):
    data_path = tmp_path / "training.csv"

    ensure_data_file(str(data_path))

    assert data_path.exists()


def test_ensure_data_file_writes_header(tmp_path):
    data_path = tmp_path / "training.csv"

    ensure_data_file(str(data_path))

    with open(data_path, "r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)

    assert header == CSV_HEADER


def test_save_training_row(tmp_path):
    data_path = tmp_path / "training.csv"
    features = [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]
    action = 1

    save_training_row(features, action, str(data_path))

    with open(data_path, "r", encoding="utf-8") as csv_file:
        rows = list(csv.reader(csv_file))

    assert len(rows) == 2
    assert rows[1][-1] == "1"


def test_save_training_row_wrong_feature_count(tmp_path):
    data_path = tmp_path / "training.csv"
    features = [0, 1, 0]
    action = 1

    with pytest.raises(ValueError):
        save_training_row(features, action, str(data_path))