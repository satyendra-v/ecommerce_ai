package com.ai.ecommerce.ai;

import com.ai.ecommerce.ai.dto.ChatRequest;
import com.ai.ecommerce.ai.dto.ChatResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

@RestController
@RequestMapping("/api/ai")
public class AiController {

    @Autowired
    private AiService aiService;

    @Value("${spring.ai.python.url}")
    private String pythonServiceUrl;

    // RestTemplate is Spring's HTTP client for making REST calls
    // In modern Spring, you'd use WebClient for reactive/non-blocking calls
    private final RestTemplate restTemplate = new RestTemplate();

    record ChatRequest(String question, String system) {}
    record ChatResponse(String answer) {}

    @PostMapping("/chat")
    public ResponseEntity<ChatResponse> chat(@RequestBody ChatRequest request) {
        String reply = aiService.chat(request.question());
        ChatResponse response = new ChatResponse(reply);
        return ResponseEntity.ok(response);
    }



    // ── MULTI-TURN CHAT WITH SESSION ──────────────────────────────────────
    record MemoryRequest(String sessionId, String message) {}

    // POST /api/chat/memory
    @PostMapping("/memory")
    public ChatResponse memoryChat(@RequestBody MemoryRequest request) {
        String url = pythonServiceUrl + "/chat/memory";
        ChatResponse response = restTemplate.postForObject(url, request, ChatResponse.class);
        return response;
    }
}
