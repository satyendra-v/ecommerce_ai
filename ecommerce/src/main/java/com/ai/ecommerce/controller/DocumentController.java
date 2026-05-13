package com.ai.ecommerce.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.*;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/documents")
public class DocumentController {

    @Value("${python.url:http://localhost:8000}")
    private String pythonServiceUrl;

    private final RestTemplate restTemplate = new RestTemplate();

    // The controller forwards the raw file bytes to the Python ingestion service.
    @PostMapping(value = "/upload", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<String> uploadDocument(
            @RequestParam("file") MultipartFile file,
            @RequestParam(value = "collection", defaultValue = "default") String collection,
            // collection = namespace for documents (e.g. "hr-policy", "product-manuals")
            @RequestParam(value = "tags", required = false) String tags
    ) throws Exception {

        // MultiValueMap is required for multipart/form-data HTTP requests.
        // Each key can have multiple values — that's the "multi" in MultiValueMap.
        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();

        // ByteArrayResource wraps raw bytes with a filename for multipart upload
        ByteArrayResource fileResource = new ByteArrayResource(file.getBytes()) {
            @Override
            public String getFilename() {
                return file.getOriginalFilename();  // Preserves original filename
            }
        };

        body.add("file", fileResource);
        body.add("collection", collection);
        if (tags != null) body.add("tags", tags);

        // Set content type to multipart/form-data for the forwarded request
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);

        ResponseEntity<String> response = restTemplate.exchange(
                pythonServiceUrl + "/rag/ingest",
                HttpMethod.POST,
                new HttpEntity<>(body, headers),
                String.class
        );
        return ResponseEntity.ok(response.getBody());
    }

    // ── LIST ALL DOCUMENTS IN A COLLECTION ───────────────────────────────
    @GetMapping("/list")
    public ResponseEntity<?> listDocuments(
            @RequestParam(defaultValue = "default") String collection
    ) {
        return ResponseEntity.ok(
                restTemplate.getForObject(
                        pythonServiceUrl + "/documents?collection=" + collection,
                        Object.class
                )
        );
    }

    // ── DELETE A DOCUMENT ─────────────────────────────────────────────────
    @DeleteMapping("/{documentId}")
    public ResponseEntity<String> deleteDocument(@PathVariable String documentId) {
        restTemplate.delete(pythonServiceUrl + "/documents/" + documentId);
        return ResponseEntity.ok("Document deleted: " + documentId);
    }
}