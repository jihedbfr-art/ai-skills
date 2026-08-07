---
name: spring-ai-tool-calling-beans
description: Architectural pattern for registering Java methods as AI tools using Spring AI's @Bean and @Description annotations.
version: 1.0.0
---

# Spring AI Tool Calling via @Bean

## Architectural Purpose
Allowing an LLM to execute backend functions (Tool Calling / Function Calling) is the foundation of Agentic architecture. Spring AI abstracts provider-specific tool schemas (OpenAI, Anthropic) by allowing developers to simply expose standard Java `@Bean` methods returning `java.util.function.Function`.

---

## 1. Core Pattern / Implementation

### Defining the Tool
Register a standard Java `Function` as a Spring `@Bean` and decorate it with `@Description`. The description is automatically converted into the JSON Schema sent to the LLM.

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Description;
import java.util.function.Function;

@Configuration
public class AiToolConfiguration {

    public record PaymentRequest(String accountId, Double amount) {}
    public record PaymentResponse(String transactionId, String status) {}

    @Bean
    @Description("Process a refund for a specific customer account")
    public Function<PaymentRequest, PaymentResponse> processRefundTool() {
        return request -> {
            // Internal business logic
            return new PaymentResponse("TXN-" + System.currentTimeMillis(), "SUCCESS");
        };
    }
}
```

### Binding to the ChatClient
```java
String response = chatClient.prompt()
    .user("Refund $50 to account ACC-987")
    .functions("processRefundTool")
    .call()
    .content();
```

---

## 2. Cost, Latency & Trade-offs
- **Token Math**: The `@Description` and the field names of the `PaymentRequest` record are sent in the system prompt. Keep field names descriptive but concise.
- **Latency Penalty**: Negligible overhead for serialization, but the LLM requires an extra round-trip to the provider to execute the tool and return the final answer.
- **Trade-off**: Hardcoding `functions("processRefundTool")` statically binds the tool. For agents with 50+ tools, you must implement dynamic tool routing to avoid blowing up the context window.

---

## 3. Verification Checklist
- [ ] Tool inputs are strictly mapped to Java `record` classes to ensure immutability and precise JSON schema generation.
- [ ] All `@Bean` descriptions are semantically clear so the LLM understands exactly *when* to invoke the tool.
- [ ] Tool implementations catch internal exceptions and return them as string errors so the LLM can self-correct, rather than crashing the Spring context.
