import pytest
import cli

# Dummy response to simulate requests.get returning an empty list


class DummyResp:
    status_code = 200
    ok = True

    def json(self):
        return []


def test_list_items_prints_empty(monkeypatch, capsys):
    # Patch cli.requests.get so it returns our DummyResp
    monkeypatch.setattr(cli.requests, 'get', lambda *args,
                        **kwargs: DummyResp())

    # list_items doesn’t use any attributes on args, so a bare object will do
    class Args:
        pass
    args = Args()

    # Call the function directly
    cli.list_items(args)

    # Capture and assert printed output
    captured = capsys.readouterr()
    assert captured.out.strip() == '[]'