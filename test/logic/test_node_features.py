import pytest

from app.chaine.blockchain import Blockchain


@pytest.mark.parametrize('some_adresses, striped_adresses, expected', [
    ('http://192.168.0.1:5000', '192.168.0.1:5000', True),
    ('http192.168.0.1:5000', '192.168.0.1:5000', False),
    ('192.168.0.1:5000', '192.168.0.1:5000', False),
    ('salut :)', 'salut :)', False),
    ]
)
def test_register_node(some_adresses, striped_adresses, expected):
    bc = Blockchain()
    bc.register_node(some_adresses)
    assert (striped_adresses in bc.nodes) is expected

# def test_valid_chain

# def test_algo_consensus