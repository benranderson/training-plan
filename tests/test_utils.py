import pytest
import app.main.utils as u


def test_open_json():
    file_path = 'app/main/inputs/events.json'
    print(u.open_json(file_path))
    # assert u.open_json(file_path) == ''
