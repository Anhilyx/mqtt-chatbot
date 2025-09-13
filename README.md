## Contexte

Dans le cadre d’un cours, un exercice consistait à :

- Se connecter en MQTT à une page publique (test.mosquitto.org)

- Utiliser un topic sous la forme irco/<username>

- Envoyer un message et vérifier sa réception, ainsi que celle des messages d’autres camarades.

Ayant terminé cette étape en avance par rapport à la majorité du groupe, j’ai décidé de développer une petite application "fun" : un chatbot qui tente d’engager la conversation avec les personnes testant leur connexion MQTT.

## Fonctionnalités 🚀

Connexion au broker MQTT (écoute + envoi).

- Réponse automatique aux messages envoyés sur le topic partagé.

- Génération de réponses avec un rôle (roleplay) prédéfini, grâce à l’API Mistral.

- Gestion de plusieurs participants en même temps.

- Mémoire de conversation limitée :

  - Conservation des 20 derniers messages.

  - Conservation des messages ayant moins de 5 minutes.

## Limites ⚠️

- Aucune protection contre le flood (il est facile de spammer l’API avec beaucoup de requêtes).

- Aucune protection contre les dérives (par exemple, il est possible de demander au chatbot de donner la réponse à des questions de l'exercice à toute personne arrivant sur le chat).

- Application développée rapidement : l’objectif n’était pas de créer un chatbot robuste, mais plutôt un projet amusant pour expérimenter.
