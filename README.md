# Chain of Fools

[![image](https://img.shields.io/github/license/Sam-prog-sudo/sam.github.io?style=flat-square)](https://github.com/Sam-prog-sudo/Chain-of-Fools/blob/master/LICENSE)
---
## Avant-propos

Mon but: créer une blockchain, en 🐍python🐍, en moins d'une semaine.
Il s'agit de mon premier gros projet, en python, il m'a permis de progresser et d'apprendre de mes erreurs.
J'y ai découvert Flask, les algorithmes de hachages, j'ai écris des kilomètres de docstrings.  
Soyez indulgent.e 😁.

## Table des matières

- [Avant-propos](#avant-propos)  
- [Introduction](#introduction)  
- [Installation](#installation)  
  - [Prérequis](#prérequis)  
  - [Code source](#code-source)  
- [Utilisation](#utilisation)  
  - [Création de node](#création-de-node)  
  - [Miner un block](#miner-un-block)  
  - [Enregistrer des transaction](#enregistrer-des-transaction)
  - [Obtenir la blockchain](#obtenir-la-blockchain)
  - [Enregistrer un node](#enregistrer-un-node)
  - [Consensus de la blockchain](#consensus-de-la-blockchain)
- [Améliorations possibles](#améliorations-possibles)
- [FAQ](#faq)
- [License](#license)
---
## Introduction
Cette application permet de:  
- Créer des nodes (flask, serveur dev --> non-sécurisé).  
- Enregistrer des nodes sur la blockchain.  
- Vérifier la blockchain.  
- Mettre à jour la blockchain gràce aux nodes, en trouvant un consensus.  
- Miner un block.  
- Renvoyer toute la chaine.  
- Enregistrer un nouvelle transaction sur la blockchain.  
## Installation
### Prérequis

* Installer [Postman](https://www.postman.com/downloads/).  

* Installer [Python 3.8+](https://www.python.org/downloads/).  

* Activer votre environnement virtuel. Exemple avec venv:
```shell
python3 -m venv /chemin/vers/environnement/virtuel
```
**ou sous windows**  
```shell
py -m venv /chemin/vers/environnement/virtuel
```
* Installer les [modules requis](https://github.com/Sam-prog-sudo/Chain-of-Fools/blob/master/requirements.txt), dans le même dossier.  
```shell
pip install -r requirements.txt
``` 
### Code source
Plusieurs solutions s'offrent à vous (toujours vers le même dossier):  
- 👯Cloner ce repo sur votre machine local à l'aide de cette adresse:  
`https://github.com/Sam-prog-sudo/Chain-of-Fools.git`.  
- 🍴Forker ce repo.
>C'est une invitation à la [contribution](#améliorations-possibles)👋
- 💾Télécharger le repo à cette adresse:  
https://github.com/Sam-prog-sudo/Chain-of-Fools/archive/master.zip


----
## Utilisation
Lancer un Shell pour la création de nodes puis, lancer Postman pour l'envoie et le retour de requêtes.  
### Lancer l'application  
A l'aide d'un shell, lancer la commande:
```shell
python3 app/main.py
```
**ou sous windows**
```shell
py app/main.py
```
### Création de node
Commencer par démarrer au moins un serveur (node):  
> Par défaut, le numéro de port est 5000  
```shell
pipenv run python Block.py
```
```shell
pipenv run python blockchain.py -p 5001
```
```shell
pipenv run python blockchain.py --port 5002
```
### Miner un block
Pour miner un nouveau block, il faut trouver la nouvelle preuve de travail.
Pour ce faire, il faut envoyer une requête `GET` à l'adresse `http://localhost:[numéro-de-port]/mine`.  

### Enregistrer des transaction
En suivant la nomenclature du format JSON, ajouter dans le `Body` de la requête:
```
{
    "sender": "adresse de l'émetteur",
    "recipient": "adresse du bénéficiaire",
    "amount": quantité-émise (un entier relatif),
}
```
Puis, envoyer la requête `POST` à l'adresse `http://localhost:[numéro-de-port]/transactions/new`. 

### Obtenir la blockchain
Pour obtenir toutes les informations stockées sur la blockchain, il suffit d'envoyer une requête `GET` à l'adresse:  
`http://localhost:5000/chain_of_fools`.  

### Enregistrer un node
En suivant la nomenclature du format JSON, ajouter dans le `Body`de la requête. Par exemple:  
```JSON
{
    "nodes": ["http://192.168.1.1", "http://192.168.1.4"]
}
```
>NB: il s'agit d'une liste de node à rajouter.  

Pour enregistrer un nouveau node sur le réseau, il faut envoyer la requête `POST` à l'adresse  
`http://0.0.0.0:[numéro-de-port]/nodes/register`.  

### Consensus de la blockchain
>Dans le cas où il y aurait plusieurs nodes, cette requête permet d'assurer la validité de la chaine,  
à l'aide d'un algorithme de consensus.  

Pour s'assurer que le node courant détient la chaine la plus à jour (donc la plus longue),  
il suffit d'envoyer une requête `GET` à l'adresse `http://localhost:5000/nodes/resolve`.

## Améliorations possibles
Cette liste est non-exhaustive:   
- ~~(Essayer de) respecter la PEP 8~~  
- Séparer les views de la logique  
- Mettre en place des test avec pytest.  
- Générer une documentation avec sphinx.  
- Créer des nodes qui vérifient les transactions.  
- Gérer les erreurs de 'requests'.
- Améliorer l'algorithme de travail.  
- Améliorer l'algorithme de hashage.  
- Permettre une saugarde physique de la blockchain.  
- Stocker d'autres informations sur la blockchain (hors cryptomonnaie).  
- Améliorer la sécurité des nodes (une vraie passoire...).  
- Obtenir certaines informations de la blockchain (qui a fait quelle transaction, et quand; combien de block ont été miné; etc.)  
- Créer un wallet  
- (Ajouter une fonction qui vérifie un block, une fois qu'il est miné)  
- Créer un interface graphique (legos qui s'imbriquent ?)  
- Traduire la docstring en anglais et la mettre en format Napoléon.  

## FAQ

>Pourquoi une blockchain ?  

[Parce que :)](https://youtu.be/gGAiW5dOnKo)

>😱 https://sametmax.com/ 😱 ?  

😥 oui, je sais ... et nan, ça ne s'écris pas pareil.

## License
**[MIT license](http://opensource.org/licenses/mit-license.php)**
