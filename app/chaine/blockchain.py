import json
from hashlib import sha256
from time import time
from urllib.parse import urlparse

import requests


class Blockchain:
    """
    Blockchain est la classe mère: elle gère la séquence immuable de blocks.
    """
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # créer le premier block
        self.new_block(proof=1989, previous_hash=1)
        # créer un set de nodes -> idempotent
        self.nodes = set()

    @property
    def last_block(self):
        """
        last_block renvoie le dernier block de la chaine.

        :return: un block
        :rtype: <dict>
        """
        return self.chain[-1]

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        valid_proof valide la preuve.
        Pour que la preuve soit validée, il faut trouver un nombre j
        tel que le hachage de la chaine (ij) se termine par 4 zéros.

        - Encode en bytes la chaine ('dernière_preuve''preuve').
        - Fait du hachi(parmentier) puis la transforme en chaine hexa.
        - Vérifie que le hach termine par 4 zéros.

        :param last_proof: dernière preuve de travail.
        :type last_proof: <int>
        :param proof: nouvelle preuve de travail.
        :type proof: <int>
        :return: True si les 4 derniers chiffres sont '0000', sinon False.
        :rtype: <bool>
        """
        guess_bytes = f'{last_proof}{proof}'.encode()
        guess_hash = sha256(guess_bytes).hexdigest()
        return guess_hash[:4] == "0000"

    def proof_of_work(self, last_block):
        """
        Algorithme de preuve de travail.

        - Tant que la nouvelle preuve de travail n'est pas trouvée par
          le mineur, elle est incrémenté de 1.

        :param last_block: Dernier block miné.
        :type last_proof: <dict>
        :return: Nouvelle preuve de travail.
        :rtype: <int>
        """
        last_proof = last_block['proof']

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def hachage(block):
        """
        hash crée un hachage SHA-256 d'un bloc.

        - Sérialise le <dict: block> en une <str> formatée en JSON,
        puis encode la <str> en bytes pour être haché.
        - NB: La <str> doit être ordonnée, selon les clés du <dict: block>,
        sinon il y aura des hachages incohérents.
        - Hache la chaine puis renvoie une <str> composée d'hex
        - NB: sha256 n'est pas le meilleur algo d'hashage.

        :param block: le block
        :type block: <dict>
        :return: hach
        :rtype: <str>
        """
        block_bytes = json.dumps(block, sort_keys=True).encode()
        return sha256(block_bytes).hexdigest()

    def new_block(self, proof, previous_hash=None,):
        """
        new_block Créer un nouveau block dans la blockchain.

        :param proof: La preuve donnée par l'algorithme de preuve de travail.
        :type proof: <int>
        :param previous_hash: Hash du block précédent, par défaut: None.
        :type previous_hash: <str>, optional
        :return: nouveau block
        :rtype: <dict>
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hachage(self.chain[-1]),
        }

        # RàZ de la liste courante des transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        new_transaction créer une nouvelle transaction qui ira
        dans le block miné.

        :param sender: L'adresse de l'émetteur.
        :type sender: <str>
        :param recipient: L'adresse du bénéficiaire.
        :type recipient: <str>
        :param amount: La quantité.
        :type amount: <int>
        :return: L'index du bloc qui contiendra cette nouvelle transaction.
        :rtype: <int>
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    def register_node(self, address):
        """
        register_node ajoute un nouveau node à la liste des nodes.

        :param address: l'adresse IP du node. Ex: 'http://192.168.0.5:5000'
        :type address: <str>
        """
        parsed_url = urlparse(address)
        if parsed_url.scheme == 'http':
            self.nodes.add(parsed_url.netloc)
        else:
            print(f"Ladresse {parsed_url} n\'est pas valide")

    def valid_chain(self, chain):
        """
        valid_chain détermine si la blockchain courante est valide, en
        vérifiant chaque block (hash + proof of work).

        - Vérifie que 'previous_hash' contenu dans le block courant,
          correspond au hachage du block précédent.
        - Vérifie la preuve de travail grace à la méthode valid_proof.

        :param chain: La blockchain
        :type chain: <list>
        :return: True or false
        :rtype: <bool>
        """
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')

            if block['previous_hash'] != self.hachage(last_block):
                return False

            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            print("\n-----------\n")
            last_block = block
            current_index += 1

        return True

    def algo_cansensus(self):
        """
        algo_cansensus est l'algorithme qui permet un consensus
        sur la blockchain.

        La méthode va parcourir tous les nœuds pour trouver la plus longue
        chaine valide du réseau: elle deviendra la chaine par défaut,
        sur le nœud courant.
        Cette méthode s'initialise sur le nœud courrant.

        - Vérifie le statuts des nœuds/nodes du réseau.
        - Vérifie la validité des chaines présentes, à l'aide de la
          méthode valid_chain.
        - Stock dans la blockchain la chaine la plus longue.

        :return: True si l'algorithme a trouvé une plus gande chaine,
        sinon False.
        :rtype: <bool>
        """
        chances = 10
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)

        for un_node in neighbours:
            for _ in range(chances):
                try:
                    response = requests.get(f'http://{un_node}/chain_of_fools')
                except requests.exceptions.RequestException as oups:
                    print(oups, ' Retrying ...')
                    continue
                else:
                    break
            else:
                raise SystemExit("Aïe ...")

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False
