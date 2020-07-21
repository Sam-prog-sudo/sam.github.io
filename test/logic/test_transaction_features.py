# import pytest

# from app.chaine.blockchain import Blockchain




# @pytest.fixture
# def valid_transaction(sender='a', recipient='b', amount=1):
#     {
#         'sender': sender,
#         'recipient': recipient,
#         'amount': amount
#     }


# class Testransactions(TestBlockchain):

#     def test_create_transaction(self):
#         self.create_transaction()

#         transaction = self.blockchain.current_transactions[-1]

#         assert transaction
#         assert transaction['sender'] == 'a'
#         assert transaction['recipient'] == 'b'
#         assert transaction['amount'] == 1

#     def test_block_resets_transactions(self):
#         self.create_transaction()

#         initial_length = len(self.blockchain.current_transactions)

#         self.create_block()

#         current_length = len(self.blockchain.current_transactions)

#         assert initial_length == 1
#         assert current_length == 0