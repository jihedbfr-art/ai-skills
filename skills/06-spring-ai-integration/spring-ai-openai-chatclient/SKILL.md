---
format: "v2"
name: "spring-ai-openai-chatclient"
title: "Spring AI: OpenAI ChatClient and Structured Outputs"
title_fr: "Spring AI : ChatClient OpenAI et sorties structurées"
description: "The Spring AI ChatClient fluent API against OpenAI, and BeanOutputConverter for turning a model response into a typed Java object instead of a string parsed by hand."
description_fr: "L'API fluente ChatClient de Spring AI face à OpenAI, et BeanOutputConverter pour transformer une réponse du modèle en objet Java typé plutôt qu'en chaîne à parser à la main."
domain: "06-spring-ai-integration"
tags: [openai, spring-ai, java, structured-outputs, engineering]
maturity: "stable"
audience: ["backend-engineer", "ai-engineer", "coding-agent"]
requires: ["java", "maven"]
updated: "2026-09-02"
---

## Prerequisites
- Java 17 and a Spring Boot 3.2.x application.
- An OpenAI API key supplied through the environment, not committed to configuration.

## Usage

### Architectural Context

Spring AI provides a portable API (the `ChatClient`) that acts as a unified abstraction layer over various AI providers. Integrating OpenAI via Spring AI protects the enterprise from vendor lock-in. Instead of mapping directly to OpenAI's proprietary JSON structures via `RestTemplate` or `WebClient`, engineers interact with high-level Java Primitives (`Prompt`, `Message`, `ChatResponse`), while Spring AI's autoconfiguration handles the serialization, retries, and REST calls.

### 1. Setup and Dependencies

To enable the OpenAI autoconfiguration, inject the specific starter into your `pom.xml`.

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-openai-spring-boot-starter</artifactId>
</dependency>
```

Add the API key to `application.yml`:

```yaml
spring:
  ai:
    openai:
      api-key: ${OPENAI_API_KEY}
      chat:
        options:
          model: gpt-4o
          temperature: 0.7
          max-tokens: 2000
```

### 2. The ChatClient Fluent API

Spring AI `1.0.x` introduced the `ChatClient.Builder`. This fluent API is the recommended way to construct context-aware AI services. It supports default system prompts, default user text, and dynamic variable expansion.

#### Java Implementation Hook

```java
// examples/OpenAiAgentService.java
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.advisor.MessageChatMemoryAdvisor;
import org.springframework.ai.chat.memory.InMemoryChatMemory;
import org.springframework.stereotype.Service;

@Service
public class OpenAiAgentService {

    private final ChatClient chatClient;

    public OpenAiAgentService(ChatClient.Builder builder) {
        // Build a pre-configured ChatClient with conversational memory
        this.chatClient = builder
            .defaultSystem("You are a strict code reviewer. Identify bugs and suggest fixes in standard Markdown.")
            .defaultAdvisors(new MessageChatMemoryAdvisor(new InMemoryChatMemory()))
            .build();
    }

    public String reviewCode(String codeSnippet, String language) {
        return this.chatClient.prompt()
            .user(u -> u.text("Review this {lang} code:\n\n{code}")
                        .param("lang", language)
                        .param("code", codeSnippet))
            .call()
            .content();
    }
}
```

### 3. Structured Outputs with BeanOutputConverter

A major requirement for enterprise systems is converting raw LLM text into strongly typed Java Objects. Spring AI achieves this by injecting JSON schema instructions into the prompt and parsing the result via Jackson.

```java
import org.springframework.ai.converter.BeanOutputConverter;
import org.springframework.ai.chat.client.ChatClient;

public record BugReport(String severity, String description, String suggestedFix) {}

public BugReport extractBug(String userIssue, ChatClient chatClient) {
    var converter = new BeanOutputConverter<>(BugReport.class);
    
    // The converter generates the JSON schema and parsing instructions
    return chatClient.prompt()
        .user(u -> u.text("Analyze this issue: {issue}\n\n{format}")
                    .param("issue", userIssue)
                    .param("format", converter.getFormat()))
        .call()
        .entity(converter);
}
```

### 4. Execution Directives (Agent Instructions)

- **Avoid Raw Clients:** Do not construct raw `WebClient` calls to `api.openai.com`. Always use the Spring AI autoconfigured `ChatClient`.
- **Statelessness:** Remember that `InMemoryChatMemory` is for demonstration. For production environments scaling across multiple Kubernetes pods, instruct the deployment of Redis or a Database-backed `ChatMemory` implementation.
- **Error Handling:** Spring AI utilizes `RestClient` under the hood. Prepare to catch `NonTransientAiException` for hard failures (like invalid API keys) and allow Spring's default retry mechanism to handle `TransientAiException` (like 429 Too Many Requests).

---
*Architected for the autonomous enterprise. A JihedAiLabs project.*

## Inputs
- The prompt, and the Java record the answer should be materialised into.

## Outputs
- A typed object, or a parse failure surfaced as an exception rather than a malformed string.
