---
name: generative-ui-streaming-components
description: Architectural pattern for rendering dynamic, AI-generated UI components (Generative UI) to the client by streaming structural JSON and resolving components on the frontend.
version: 1.0.0
---

# Generative UI & Streaming Components

## Architectural Purpose
Instead of responding to users exclusively with markdown text, Generative UI allows AI models to respond with fully functional, interactive UI components (like a live chart, an interactive form, or a dashboard widget) similar to Claude's Artifacts or Vercel's v0.

---

## 1. Core Pattern / Implementation

The AI does not write raw React code. It returns structured intent (JSON) that the frontend maps to pre-built components.

### Backend (Model Output Schema)
Force the model to stream responses in a strict JSON format identifying the component:
```json
{
  "type": "weather_widget",
  "props": {
    "location": "Paris",
    "temperature": 22,
    "condition": "Sunny"
  }
}
```

### Frontend (Component Resolver)
React/Angular maps the streamed JSON payload to a real UI component:

```tsx
function ComponentRenderer({ payload }) {
  if (payload.type === 'weather_widget') {
    return <WeatherWidget {...payload.props} />;
  }
  if (payload.type === 'stock_chart') {
    return <StockChart data={payload.props.series} />;
  }
  return <Markdown>{payload.text}</Markdown>;
}
```

---

## 2. Cost, Latency & Trade-offs
- **Token Math**: JSON schemas consume more output tokens than raw text due to structural overhead (brackets, keys). 1 token ≈ 2 characters in JSON.
- **Latency Penalty**: To maintain perceived performance, the frontend must support streaming JSON parsing (e.g., yielding partial JSON blocks as they arrive) rather than waiting for the entire TTFT of the JSON object.
- **Trade-off**: Requires strict schema adherence. If the LLM hallucinates a prop name, the React component may crash. Strict fallback error boundaries are required.

---

## 3. Verification Checklist
- [ ] LLM output is constrained to a predefined JSON schema or specific tool call.
- [ ] Frontend implements React Error Boundaries around dynamically generated components.
- [ ] Streaming parser gracefully handles partial/incomplete JSON chunks.
