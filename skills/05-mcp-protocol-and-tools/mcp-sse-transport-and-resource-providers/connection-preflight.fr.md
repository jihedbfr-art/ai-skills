# Vérifier une connexion MCP avant de confier des outils à un agent

[English version](connection-preflight.md)

Consigner d'abord le commit du serveur, la version du SDK, celle du protocole et le transport. Un endpoint de santé HTTP fonctionnel ne prouve rien sur les droits d'un outil. Une connexion réussie ne garantit pas non plus la qualité de son résultat.

## Identifier le transport

Pour le protocole 2025-11-25, distinguer stdio de Streamable HTTP. SSE peut transporter une réponse Streamable HTTP ; sa présence seule n'identifie pas l'ancien transport à deux endpoints. Dans la version MCP Guard testée, la connexion historique utilise `/sse` et `/mcp/message` ; un POST sur `/mcp` n'est pas son chemin d'appel.

Utiliser le endpoint documenté par le serveur et un client MCP qui négocie une version prise en charge. En stdio, vérifier la commande de lancement, le répertoire de travail et l'environnement ; les messages du protocole vont sur stdout, les diagnostics sur stderr.

## Consigner chaque frontière séparément

| Contrôle | Preuve à conserver |
|---|---|
| Initialiser et découvrir les outils | Version négociée et noms des outils ; masquer les identifiants |
| Valider les arguments | Une entrée valide et une entrée invalide avec un résultat explicite |
| Lire un résultat | Erreurs JSON-RPC et `result.isError` vérifiés avant d'utiliser le contenu |
| Exercer les droits | Un appel interdit échoue côté serveur même si l'agent le demande |
| Séparer les appelants | Le lecteur reste refusé après un appel administrateur et avec des clients concurrents |
| Borner les nouvelles tentatives | Timeout et refus remontés ; aucune répétition automatique d'un effet métier |

Tester les outils qui modifient des données avec une fixture inerte ou une ressource jetable. Consigner l'action réellement effectuée en plus de la réponse. Un timeout laisse le résultat incertain ; vérifier si l'opération a eu lieu avant de la répéter.

## Rejouer la référence vérifiée

Java 17, Maven et Docker sont nécessaires. Utiliser un nouveau clone :

```bash
git clone https://github.com/jihedbfr-art/mcp-keycloak-guard.git
cd mcp-keycloak-guard
git checkout 177fdef
mvn verify
```

Les cinq tests d'intégration de cette version ont été rejoués localement le 14 octobre 2026. Ils couvrent les requêtes sans authentification ou avec jeton invalide, un appelant sans rôle MCP, les résultats lecteur/administrateur et l'isolation de clients concurrents. Le refus de l'outil administrateur au lecteur est une erreur d'outil MCP, pas une hypothèse de réponse HTTP 403. Ces tests ne démontrent ni le rejet d'une mauvaise audience, ni l'isolation des jetons transmis en aval, ni la prise en charge de Streamable HTTP.

## Sources et coût

Utiliser les [transports MCP](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports) pour le périmètre du protocole et la [gestion des erreurs d'outils](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) pour interpréter les résultats. La [PR de référence](https://github.com/jihedbfr-art/mcp-keycloak-guard/pull/1) n'est pas une release publiée. Un test Docker local prend plus de temps qu'un contrôle de schéma, mais il exerce ensemble l'authentification et l'invocation asynchrone. Le rejouer quand ces frontières changent ; garder un petit contrôle inerte pour les vérifications courantes de connexion.

---

<div align="center">
  <img src="../../../assets/brand/jihedailabs-logo.svg" alt="JihedAiLabs" width="120">
  <br>
  <sub>Un projet <a href="https://github.com/jihedbfr-art"><b>JihedAiLabs</b></a></sub>
</div>
