---
format: "v2"
name: "spring-ai-chatclient-advisors"
title: "Spring AI ChatClient Advisors"
title_fr: "Spring AI ChatClient Advisors"
description: "Enterprise Java patterns for Spring AI 1.0 using ChatClient fluent API, Advisors chain, and Spring Data PGVector."
description_fr: "Patterns Java d'entreprise pour Spring AI 1.0 utilisant l'API fluide ChatClient, la chaîne d'Advisors et Spring Data PGVector."
domain: "06-spring-ai-integration"
tags: [cybersecurity, engineering, best-practices]
maturity: "stable"
audience: ["backend-engineer", "security-engineer", "coding-agent"]
requires: ["bash", "git"]
updated: "2026-08-08"
---



## Prerequisites
- Target system, dependencies and environment configured.

## Usage
### Architectural Purpose
Spring AI provides a unified, enterprise-ready Java abstraction for interacting with AI models. The `ChatClient` fluent API paired with `Advisor` interceptors allows seamless context enhancement, chat memory management, and structured output parsing.

---

### 1. Spring Boot 3 & Spring AI 1.0 Setup

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-model-anthropic</artifactId>
    <version>1.0.0-M5</version>
</dependency>
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-pgvector-store-spring-boot-starter</artifactId>
    <version>1.0.0-M5</version>
</dependency>
```

---

### 2. Fluent ChatClient Configuration

```java
@Service
public class CustomerSupportAiService {

    private final ChatClient chatClient;

    public CustomerSupportAiService(ChatClient.Builder builder, VectorStore vectorStore) {
        this.chatClient = builder
                .defaultSystem("You are a technical support architect for Telecom systems.")
                .defaultAdvisors(
                        new MessageChatMemoryAdvisor(new InMemoryChatMemory()),
                        new QuestionAnswerAdvisor(vectorStore, SearchRequest.query("").withTopK(4))
                )
                .build();
    }

    public String processQuery(String conversationId, String userMessage) {
        return this.chatClient.prompt()
                .user(userMessage)
                .advisors(a -> a.param(MessageChatMemoryAdvisor.CHAT_MEMORY_CONVERSATION_ID_KEY, conversationId))
                .call()
                .content();
    }
}
```

---

### 3. Production Advantages

- **Clean Decoupling**: Provider-agnostic API. Switch between Anthropic, OpenAI, or Ollama without modifying application service logic.
- **Interception Chain**: `Advisor` pipeline handles RAG insertion, chat memory persistence, and token logging automatically.
- **Native Spring Integration**: Integrates directly with Spring Security, Spring Metrics, and Micrometer tracing.

## Inputs
- Relevant source code, logs, network traces, or system specifications.

## Outputs
- Analysis findings, security audit report, or generated code artifacts.