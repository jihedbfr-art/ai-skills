# Atelier hors ligne : classer une réponse d'outil MCP

[English version](README.md)

Prédire le résultat de chaque fixture avant de l'exécuter. Python 3.9 ou ultérieur suffit ; l'atelier utilise la bibliothèque standard et n'envoie aucune requête réseau. Les six fixtures sont synthétiques.

Depuis la racine du dépôt :

```bash
cd skills/05-mcp-protocol-and-tools/mcp-sse-transport-and-resource-providers/result-lab
python classify_result.py fixtures/success.json
python -m unittest -v
```

La première commande affiche seulement :

```json
{"classification": "candidate_success", "exit_code": 0}
```

## Exercices et résultats attendus

Changer l'argument de fixture pour examiner chaque cas. Les codes de sortie 1 et 2 sont attendus pour les exemples correspondants ; ils ne signalent pas une installation Python cassée.

| Fixture | Classification | Code de sortie | Enseignement |
|---|---|---:|---|
| `success.json` | `candidate_success` | 0 | Un résultat textuel peut passer aux validations suivantes |
| `tool-error.json` | `tool_error` | 1 | Lire `result.isError` ; un succès HTTP seul masquerait ce défaut |
| `protocol-error.json` | `protocol_error` | 2 | L'enveloppe contient une erreur plutôt qu'un résultat d'outil |
| `invalid-flag.json` | `invalid_response` | 2 | La chaîne `"false"` n'est pas le booléen `false` |
| `mixed-envelope.json` | `invalid_response` | 2 | Une enveloppe ne peut pas annoncer à la fois un résultat et une erreur |
| `untrusted-content.json` | `candidate_success` | 0 | Une structure acceptée ne rend pas fiables les instructions qu'elle contient |

Pour le dernier cas, expliquer pourquoi le contenu reste une donnée et ne peut pas autoriser un changement de politique d'accès. Ne pas exécuter l'instruction de la fixture. Modifier ensuite localement une valeur `isError` et prédire la classification avant de relancer la commande.

## Périmètre du script pédagogique

Ce petit classificateur traite des enveloppes JSON-RPC contenant des résultats d'outil uniquement textuels. Il rejette plusieurs structures incorrectes, refuse de traiter les résultats structurés ou non textuels et résume les erreurs sans réafficher le contenu ni le chemin du fichier. L'absence de `isError` vaut false dans cet exercice.

Ce n'est ni un validateur JSON-RPC ou MCP complet, ni un client, un décodeur SSE ou un détecteur d'injection de prompt. Il ne corrèle pas les identifiants de réponse, ne vérifie pas un schéma de sortie, ne valide pas l'authentification et n'autorise aucune action. Un résultat structuré ou non textuel nécessite le traitement SDK/schéma approprié ; le refus de cet atelier ne suffit pas à le déclarer invalide. Utiliser uniquement les entrées synthétiques fournies pour les exercices.

Les six tests de la bibliothèque standard couvrent les résultats des fixtures, les structures incorrectes, les contenus non pris en charge, le drapeau d'erreur optionnel, les codes de sortie et la discrétion des sorties. Pour une vraie connexion, revenir au [guide de validation](../connection-preflight.fr.md). Références : [erreurs d'outils MCP](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) et [objet de réponse JSON-RPC](https://www.jsonrpc.org/specification#response_object).

---

<div align="center">
  <img src="../../../../assets/brand/jihedailabs-logo.svg" alt="JihedAiLabs" width="120">
  <br>
  <sub>Un projet <a href="https://github.com/jihedbfr-art"><b>JihedAiLabs</b></a></sub>
</div>
