package com.ai.ecommerce.controller;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

@RestController
@RequestMapping("/api/gateway")
public class GatewayController {

    @Value("${spring.ai.python.url:http://localhost:8000}")
    private String pythonUrl;

    private final RestTemplate restTemplate = new RestTemplate();

    private final ExecutorService executor = Executors.newCachedThreadPool();

    public record ChatRequest(String sessionId, String message, String userId) {}

    // Standard Chat
    @PostMapping("/chat")
    public ResponseEntity<Map> chat(@RequestBody ChatRequest req) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        HttpEntity<ChatRequest> httpEntity = new HttpEntity<>(req, headers);

        ResponseEntity<Map> response = restTemplate.exchange(
                pythonUrl + "/chat",
                HttpMethod.POST,
                httpEntity,
                Map.class
        );
        return ResponseEntity.ok(response.getBody());
    }

    // SSE Stream Chat for long-running agent tasks
    @GetMapping(value = "/chat/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public SseEmitter streamChat(
            @RequestParam String sessionId,
            @RequestParam String message
    ) {
        // SseEmitter timeout: 5 minutes for long-running agent tasks
        SseEmitter emitter = new SseEmitter(300_000L);

        executor.execute(() -> {
            try {
                // Forward the SSE stream from Python service to the client
                // In production use WebClient (reactive) for non-blocking streaming
                restTemplate.execute(
                        pythonUrl + "/chat/stream?sessionId=" + sessionId + "&message=" + message,
                        HttpMethod.GET,
                        null,
                        response -> {
                            byte[] buffer = new byte[256];
                            int n;
                            while ((n = response.getBody().read(buffer)) != -1) {
                                String chunk = new String(buffer, 0, n);
                                emitter.send(SseEmitter.event().data(chunk));
                            }
                            emitter.complete();
                            return null;
                        }
                );
            } catch (Exception e) {
                emitter.completeWithError(e);
            }
        });
        return emitter;
    }
}
