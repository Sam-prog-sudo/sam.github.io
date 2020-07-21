import hashlib
import json
from time import time
import pytest

from app.chaine.blockchain import Blockchain


@pytest.fixture
def first_block():
    return {
        'index': 1,
        'timestamp': time(),
        'transactions': [],
        'proof': 1989,
        'previous_hash': 1,
     }


def test_initialization_blockchain(first_block):
    bc = Blockchain()
    assert bc.chain[0]['index'] == first_block['index']
    assert isinstance(
        bc.chain[0]['timestamp'],
        type(first_block['timestamp'])
    )
    assert bc.chain[0]['transactions'] == first_block['transactions']
    assert bc.chain[0]['proof'] == first_block['proof']
    assert bc.chain[0]['previous_hash'] == first_block['previous_hash']


def test_last_block():
    bc = Blockchain()
    assert bc.last_block == bc.chain[-1]


@pytest.fixture
def a_valid_block():
    block_1 = {
        'index': 2,
        'timestamp': time(),
        'transactions': [],
        'proof': 123,
        'previous_hash': 'abc',
    }
    return block_1


@pytest.fixture
def an_invalid_block():
    block_2 = {
        'index': 'salut',
        'timestamp': list('cava',),
        'transactions': 22,
        'proof': None,
        'previous_hash': 46,
    }
    return block_2


@pytest.mark.parametrize('some_blocks', [
    'a_valid_block',
    'an_invalid_block'
    ]
)
def test_hachage(some_blocks):
    bc = Blockchain()
    block_json = json.dumps(
        some_blocks,
        sort_keys=True
        ).encode()
    hash_test = hashlib.sha256(block_json).hexdigest()

    assert len(hash_test) == 64
    assert isinstance(
        hash_test,
        type(bc.hachage(some_blocks))
        )
    assert hash_test == bc.hachage(some_blocks)


def test_block_creation(a_valid_block, proof=123, previous_hash='abc'):
    bc = Blockchain()
    block_a_tester = bc.new_block(proof, previous_hash)

    assert block_a_tester['index'] == a_valid_block['index']
    assert isinstance(
        block_a_tester['timestamp'],
        type(a_valid_block['timestamp'])
        )
    assert block_a_tester['proof'] == a_valid_block['proof']
    assert block_a_tester['previous_hash'] == a_valid_block['previous_hash']
