<p align="center">
  <img src="assets/jihedailabs-logo.svg" width="180" alt="Logo JihedAiLabs" />
</p>

<h1 align="center">AI Engineering Skills Library</h1>

<p align="center">
  <b>Base de connaissances opérationnelle pour l'ingénierie des systèmes IA, agents LLM, pipelines RAG et intégrations Model Context Protocol (MCP).</b>
</p>

<p align="center">
  <a href="README.md">🇬🇧 Read in English</a> •
  <a href="#-architecture--domaines">Architecture</a> •
  <a href="#-conventions">Conventions</a> •
  <a href="#-licence">Licence</a>
</p>

---

## 📌 Présentation

Ce dépôt rassemble **32 compétences d'ingénierie IA (skills)** réparties sur **15 domaines clés**, en croissance vers un plafond de 5 skills par domaine. Chaque fiche suit un format hybride : des recommandations d'architecture claires pour l'humain et des patterns directement exploitables par les assistants d'ingénierie et développeurs.

Il fait le pont entre la théorie de l'IA et la réalité de la production en entreprise (économie des tokens, compromis de latence, gestion d'état, garde-fous de sécurité et intégration Spring AI).

---

## 🏗️ Architecture & Domaines

```text
ai-skills/
├── 01-llm-foundations-and-models/     # Sélection des modèles, optimisation du contexte, quantification & calculs de tokens
├── 02-prompt-and-context-engineering/# Few-shot, Chain-of-Thought, ReAct, délimiteurs XML & compression de contexte
├── 03-rag-architectures/              # Stratégies de découpage (chunking), recherche hybride, reranking par cross-encoder & GraphRAG
├── 04-agentic-workflows/              # Orchestration mono/multi-agents, boucles de supervision, réflexion & appels d'outils parallèles
├── 05-mcp-protocol-and-tools/         # Serveurs Model Context Protocol (MCP), transports stdio/SSE & schémas d'outils
├── 06-spring-ai-integration/          # Spring AI ChatClient, Advisors, Tool Calling `@Bean` & intégration PGVector
├── 07-vector-databases-and-embeddings/# Modèles d'embeddings, indexation HNSW, tuning PGVector & métriques de similitude
├── 08-ai-security-and-guardrails/     # Défense contre le prompt injection, masquage PII, prévention de fuite de secrets & rate limits
├── 09-evaluations-and-observability/  # Métriques RAGAS, LLM-as-a-judge comparatif, tests de non-régression & traçage OpenTelemetry
├── 10-coding-agents-and-workflow/     # Flux de travail des agents de code, conformité Git-human & refactoring
├── 11-custom-mcp-development/         # Création de serveurs MCP en Python/TS, providers de ressources et outils sur-mesure
├── 12-low-code-ai-workflows/          # Workflows n8n, Flowise, Dify, orchestration visuelle d'agents et pipelines
├── 13-ai-ux-and-frontend/             # Interfaces génératives, Claude artifacts, v0.dev, et UX orientée agent
├── 14-multimedia-and-generation/      # Serveurs MCP Vidéo/Audio, automatisation PPTX, agents multimodaux Sora/Runway
└── 15-frontier-models-and-trends/     # Comparatifs de modèles de raisonnement, budgets de compute à l'inférence & contexte géant
```

---

## 📋 Matrice des Domaines

| Domaine | Skills | Thème Principal | Sujets Couverts |
| :--- | :---: | :--- | :--- |
| **01. LLM Foundations** | 2 | Modèles & Économie | Calculs de tokenization, dégradation du contexte, quantification (GGUF/AWQ), coûts API |
| **02. Prompt & Context Eng.** | 2 | Optimisation de Prompt | Architecture du prompt système, délimiteurs XML, ReAct, troncature de contexte |
| **03. RAG Architectures** | 4 | Recherche Avancée | Chunking sémantique, hybride BM25 + Vector, reranking cross-encoder, GraphRAG |
| **04. Agentic Workflows** | 4 | Orchestration Multi-Agents | Persistance de graphe d'état, pattern supervisor, réflexion, outils parallèles |
| **05. MCP & Tooling** | 2 | Spécification Protocole | Serveur MCP, transport stdio/SSE, schémas d'outils JSON-Schema |
| **06. Spring AI Integration** | 2 | IA Java Entreprise | API fluide `ChatClient`, chaîne d'Advisors, Spring Data PGVector, Tool Calling `@Bean` |
| **07. Vector DB & Embeddings**| 2 | Optimisation Stockage | Compromis dimensionnels d'embeddings, indexation HNSW, Cosine vs Produit Scalaire |
| **08. AI Security** | 2 | Sécurité & Garde-Fous | Prompt injection indirect, assainissement de sortie, masquage PII, rate-limiting |
| **09. Evals & Observabilité** | 4 | Qualité & Métriques | RAGAS, LLM-as-judge comparatif, jeu de données étalon (CI), spans OpenTelemetry |
| **10. Coding Agents** | 2 | Productivité Développeur | Flux d'agents autonomes, hygiène des commits Git, génération de tests |
| **11. Custom MCP** | 1 | Extension de Contexte | Création de serveur MCP Python/TS, APIs personnalisées, routage SSE/stdio |
| **12. Low-Code AI** | 1 | Workflows Visuels | Orchestration n8n, pipelines Dify, logique de branchement |
| **13. AI UX & Frontend** | 1 | Interfaces Génératives | Claude artifacts, UI v0.dev, rendu de composants en streaming |
| **14. Multimedia AI** | 1 | Contenu Enrichi | Flux vidéo Sora, automatisation PPTX, synthèse audio |
| **15. Frontier Models** | 2 | Évaluation & Coût des Modèles | Comparatifs de capacités entre modèles de raisonnement, budgets de compute |

---

## 📐 Conventions & Engagements

Chaque fiche de ce dépôt respecte 4 contraintes d'ingénierie strictes :

1. **Estimation des Coûts et Latences** : Chaque technique précise son impact en consommation de tokens, sa pénalité de latence (TTFT / TBT) et sa complexité de maintenance.
2. **Versionnage des APIs** : Toutes les bibliothèques citées (Spring AI, LangChain, Anthropic SDK, OpenAI SDK) mentionnent explicitement leur version cible.
3. **Zéro Contenu Superflu** : Chaque domaine croît vers un plafond de **5 skills à fort impact** — une fiche n'est ajoutée que si elle couvre un pattern réellement distinct, jamais pour gonfler le compteur.
4. **Zéro Trace d'IA** : L'ensemble de la documentation adopte une voix technique naturelle et rigoureuse ancrée dans l'expérience du terrain.

---

## 📄 Licence

Distribué sous licence **MIT**. Conçu & entretenu par **Jihed Ben Arfa**.
