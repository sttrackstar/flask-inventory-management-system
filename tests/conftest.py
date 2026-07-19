import os
import sys
import pytest

# 1) Compute project root (one level up from this tests/ folder)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# 2) Prepend it to sys.path so Python can find your `app/` package
if project_root not in sys.path:
    sys.path.insert(0, project_root)


@pytest.fixture
def client():
    from app import create_app

    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()