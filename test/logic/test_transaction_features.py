import pytest

from app.chaine.blockchain import Blockchain


@pytest.fixture
def one_transaction():
    bc = Blockchain()
    bc.new_transaction('a', 'b', 1)


def test_create_transaction():
    bc = Blockchain()
    bc.new_transaction('a', 'b', 1)
    transaction = bc.current_transactions[-1]

    assert transaction
    assert transaction['sender'] == 'a'
    assert transaction['recipient'] == 'b'
    assert transaction['amount'] == 1


def test_resets_current_transactions_when_mined():
    bc = Blockchain()
    bc.new_transaction('a', 'b', 1)

    initial_length = len(bc.current_transactions)

    bc.new_block(123, 'abc')

    current_length = len(bc.current_transactions)

    assert initial_length == 1
    assert current_length == 0
