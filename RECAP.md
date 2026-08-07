# 📊 RECAP — ai-skills Engineering Knowledge Base

> Document récapitulatif interne de la structure, des vagues de rédaction et des règles d'ingénierie du dépôt `ai-skills`.

## 1. Vue d'ensemble du Dépôt

* **Nom** : `ai-skills`
* **Marque Perso** : JihedAiLabs (`assets/jihedailabs-logo.svg`)
* **Format** : Fiches `SKILL.md` hybrides (Guide d'architecture humain + procédure exploitable par agent).
* **Volumétrie** : 10 domaines x 5 skills = 50 skills ciblés à haute valeur ajoutée.
* **Langues** : Bilingue (Skills en Anglais technique, READMEs en EN et FR).

---

## 2. Tableau de Suivi des 10 Domaines (Roster 50/50)

| ID | Domaine | Statut Roster | Skills Rédigés | Total Visé |
| :--- | :--- | :---: | :---: | :---: |
| `01-llm-foundations-and-models` | LLM Selection & Economics | 🟢 Prêt | 5 / 5 | 5 |
| `02-prompt-and-context-engineering` | Prompting & Context Window | 🟢 Prêt | 5 / 5 | 5 |
| `03-rag-architectures` | Advanced Retrieval & Hybrid Search | 🟢 Prêt | 5 / 5 | 5 |
| `04-agentic-workflows` | Multi-Agent & State Graphs | 🟢 Prêt | 5 / 5 | 5 |
| `05-mcp-protocol-and-tools` | Model Context Protocol & Tools | 🟢 Prêt | 5 / 5 | 5 |
| `06-spring-ai-integration` | Enterprise Java Spring AI | 🟢 Prêt | 5 / 5 | 5 |
| `07-vector-databases-and-embeddings` | Embeddings & PGVector Tuning | 🟢 Prêt | 5 / 5 | 5 |
| `08-ai-security-and-guardrails` | Guardrails & Prompt Injection | 🟢 Prêt | 5 / 5 | 5 |
| `09-evaluations-and-observability` | RAGAS & OpenTelemetry Tracing | 🟢 Prêt | 5 / 5 | 5 |
| `10-coding-agents-and-workflow` | Agentic Coding & Git Hygiene | 🟢 Prêt | 5 / 5 | 5 |
| **TOTAL** | **10 Domaines** | **🟢 10/10** | **50 / 50** | **50** |

---

## 3. Charte d'Ingénierie & Règles Stricte

1. **Coûts & Latences** : Nommer systématiquement l'impact en tokens, la latence au premier token (TTFT) et la complexité d'infrastructure.
2. **Versionnage API** : Préciser les versions de Spring AI (3.x / 1.0 M-series), OpenAI SDK (v1.x), Anthropic SDK (v0.x).
3. **Zéro Trace d'IA** : Style direct, neutre, concis, évitant la redondance et la sur-explication.
4. **Git Hygiene** : Un commit par skill ou lot cohérent, signé `Jihed Ben Arfa <your.email@example.com>`.
