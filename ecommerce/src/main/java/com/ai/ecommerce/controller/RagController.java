package com.ai.ecommerce.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import java.util.Map;

@RestController
@RequestMapping("/api/rag")
public class RagController {

    @Value("${python.url:http://localhost:8000}")
    private String pythonServiceUrl;

    private final RestTemplate restTemplate = new RestTemplate();

    record QueryRequest(
        String question,
        String collection,   // which document collection to search
        int topK,            // how many chunks to retrieve (default 4)
        boolean citeSources  // whether to include source references in answer
    ) {}

    // POST /api/rag/query
    // Ask a question against the document collection
    @PostMapping("/query")
    public ResponseEntity<Map> query(@RequestBody QueryRequest req) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        ResponseEntity<Map> response = restTemplate.exchange(
            pythonServiceUrl + "/query",
            HttpMethod.POST,
            new HttpEntity<>(req, headers),
            Map.class
        );
        return ResponseEntity.ok(response.getBody());
    }
}