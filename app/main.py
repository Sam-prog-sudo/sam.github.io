from argparse import ArgumentParser
from uuid import uuid4

from flask import Flask, jsonify, request

from app.chaine.blockchain import Blockchain

app = Flask(__name__)
# Générer une adresse unique pour ce nœud
# uuid4 est globalement plus aléatoire/unique que uuid1
node_identifier = str(uuid4()).replace('-', '')
# Instantie la Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    """
    mine permet de miner un nouveau block.
    Elle est déclenchée par le endpoint /mine (requête GET)

    - exécute l'algorithme de preuve de travail.
    - reçoit une récompense (un coin/une pièce) pour avoir trouvé la preuve.
    - L'expéditeur est "0" pour signifier que c'est le nœud qui a extrait une
    nouvelle pièce/coin.
    - Fabrique le nouveau bloc en l'ajoutant à la chaîne

    :return: réponse en JSON contenant les informations sur le nouveau block
    et le hash précédent (immuabilité de la blockchain), et un code 200 OK.
    :rtype: <JSON>
    """
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    previous_hash = blockchain.hachage(last_block)
    block = blockchain.new_block(proof, previous_hash)

    reponse = {
        'message': "Nouveau block miné",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(reponse), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """
    new_transaction permet d'ajouter les données d'une
    nouvelle transaction, en format JSON.
    Elle est déclenchée par le endpoint /transactions/new (requête POST).

    - Vérifie que les valeurs demandée dans la requête sont dans les données
    envoyées en POST. Renvoie un code 400 Bad Request, le cas échéant.
    - Créé une nouvelle transaction dans un block

    :return: réponse en JSON contenant un message de confirmation et
    un code '201 Created'.
    :rtype: <JSON>
    """
    valeurs = request.get_json()

    demande = ['sender', 'recipient', 'amount']
    if not all(k in valeurs for k in demande):
        return 'Valeurs manquantes', 400

    t1 = all(
        isinstance(s, str) for s in [
            valeurs['sender'],
            valeurs['recipient']
            ]
        )
    t2 = isinstance(valeurs['amount'], int)

    if t1 and t2:
        index = blockchain.new_transaction(
            valeurs['sender'],
            valeurs['recipient'],
            valeurs['amount'],
            )
    else:
        return 'Valeurs érronés', 400

    reponse = {
        'message': f'Ajout d\'une nouvelle transaction au block {index}'
        }
    return jsonify(reponse), 201


@app.route('/chain_of_fools', methods=['GET'])
# https://youtu.be/gGAiW5dOnKo
def full_chain():
    """
    full_chain permet d'obtenir toute la chaine et sa longueur.
    Elle est déclenchée par le endpoint /chain_of_fools (requête GET).

    :return: réponse en JSON contenant la chaine et sa longueur + code 200 OK
    :rtype: <JSON>
    """
    reponse = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(reponse), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    """
    register_nodes permet d'enregistrer au moins un nouveau node,
    en format JSON.
    Elle est déclenchée par le endpoint /nodes/register (requête POST).

    - Vérifie que les valeurs envoyé dans la requête POST existe.
    Renvoie un code 400 Bad Request, le cas échéant.
    - Enregistre les nodes grace à la méthode register_node.

    :return: réponse en JSON contenant un message de confirmation,
    la liste des nodes et un code 201 Created.
    :rtype: <JSON>
    """
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Erreur: Veuillez fournir une liste valide de nœuds", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'Au mois un nouveau node a été ajouté.',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    """
    consensus regarde si la chaine courante fait consensus.
    Elle est déclenchée par le endpoint /nodes/resolve (requête GET).

    :return: réponse en JSON contenant un message spécifiant la chaine
    faisant autorité, et un code 200 OK.
    :rtype: <JSON>
    """
    replaced = blockchain.algo_cansensus()

    if replaced:
        response = {
            'message': 'La chaine courante a été remplacée.',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'La chaine courante fait authorité.',
            'chain': blockchain.chain
        }
    return jsonify(response), 200


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument(
        '-p', '--port', default=5000, type=int, help='port to listen on'
        )
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
