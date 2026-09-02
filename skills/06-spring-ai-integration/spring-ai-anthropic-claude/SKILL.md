---
format: "v2"
name: "spring-ai-anthropic-claude"
title: "Spring AI: Anthropic Claude Integration"
title_fr: "Spring AI : intégration d'Anthropic Claude"
description: "Wiring Anthropic Claude into a Spring Boot application through Spring AI, including tool calling and the cost model that decides how much context you can afford."
description_fr: "Brancher Anthropic Claude dans une application Spring Boot via Spring AI, avec le tool calling et le modèle de coût qui décide du contexte que l'on peut se permettre."
domain: "06-spring-ai-integration"
tags: [anthropic, spring-ai, java, tool-calling, engineering]
maturity: "stable"
audience: ["backend-engineer", "ai-engineer", "coding-agent"]
requires: ["java", "maven"]
updated: "2026-09-02"
---

## Prerequisites
- Java 17 and a Spring Boot 3.2.x application.
- An Anthropic API key reaching the application from the environment, never from application.yml.

## Usage

### Architectural Context

Anthropic's Claude models (particularly the 3.5 Sonnet and 3.7 families) are heavily favored in enterprise environments due to their massive 200,000-token context windows, rigorous steering constraints (Constitutional AI), and unparalleled performance in complex software architecture generation. 

Spring AI abstracts the Anthropic Messages API, allowing Java developers to seamlessly integrate Claude using the standard `ChatClient`, while also leveraging Spring AI's automatic Tool Calling (`@Tool`) capabilities.

### 1. Setup and Dependencies

Inject the Anthropic starter into your Maven `pom.xml`.

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-anthropic-spring-boot-starter</artifactId>
</dependency>
```

Configure your Anthropic API key and the target model in `application.yml`. Claude 3.5 Sonnet is the recommended default for balancing speed and profound intelligence.

```yaml
spring:
  ai:
    anthropic:
      api-key: ${ANTHROPIC_API_KEY}
      chat:
        options:
          model: claude-3-5-sonnet-20241022
          temperature: 0.2 # Lower temperature for exact code/data extraction
          max-tokens: 4096
```

### 2. Java Implementation Hook: Function Calling

A core strength of Claude combined with Spring AI is deterministic Function Calling. You can define a Java `Function` or use `@Tool`, and Spring AI will automatically translate it into Claude's tool schema.

```java
// examples/ClaudeFinancialAgent.java
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Description;
import org.springframework.stereotype.Service;
import java.util.function.Function;

@Service
public class ClaudeFinancialAgent {

    private final ChatClient chatClient;

    public ClaudeFinancialAgent(ChatClient.Builder builder) {
        this.chatClient = builder
            .defaultSystem("You are a financial analyst agent. Use the provided tools to retrieve real-time stock prices.")
            .build();
    }

    public String analyzePortfolio(String userQuery) {
        // The chat client automatically binds the function "getStockPrice" 
        // to the Claude API request as an available tool.
        return this.chatClient.prompt()
            .user(userQuery)
            .functions("getStockPrice") 
            .call()
            .content();
    }
}

// In a Configuration class:
import org.springframework.context.annotation.Configuration;

@Configuration
class ToolConfiguration {

    public record StockRequest(String tickerSymbol) {}
    
    @Bean
    @Description("Gets the current stock price in USD for a given ticker symbol")
    public Function<StockRequest, Double> getStockPrice() {
        return request -> {
            // Mock implementation. In reality, calls an external REST API.
            if (request.tickerSymbol().equalsIgnoreCase("AAPL")) return 150.0;
            if (request.tickerSymbol().equalsIgnoreCase("MSFT")) return 300.0;
            return 0.0;
        };
    }
}
```

### 3. Financial Modeling (Claude 3.5 Sonnet)

Always architect your agent loops with cost awareness. Claude's pricing is asymmetrical to penalize massive outputs.

- **Input Tokens:** $3.00 per 1M tokens.
- **Output Tokens:** $15.00 per 1M tokens.

**Enterprise Heuristic:** When analyzing a massive 150k token codebase, instruct Claude to output *only* the specific lines of code that need changing, rather than rewriting entire files. Output tokens are 5x more expensive than input tokens.

### 4. Execution Directives (Agent Instructions)

- **System Prompts:** Unlike DeepSeek-R1, Claude heavily respects the System Prompt. Use it to define strict behavioral constraints and formatting rules.
- **XML Tagging:** Anthropic models are explicitly trained to recognize and output XML tags. If you need Claude to parse a specific section of a prompt, wrap it in `<context></context>` or `<codebase></codebase>` tags.

---
*Architected for the autonomous enterprise. A JihedAiLabs project.*

## Inputs
- The Spring Boot module to integrate, and the Java methods to expose as callable tools.

## Outputs
- A configured ChatClient, tool-calling beans registered with the model, and a per-request cost estimate.
