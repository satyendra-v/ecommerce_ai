package com.ai.ecommerce.ai;

import org.springframework.stereotype.Service;

@Service
public class AiServiceImpl implements AiService {

    @Override
    public String chat(String prompt) {
        // TODO: integrate with an AI provider (OpenAI, local model, etc.)
        if (prompt == null || prompt.isEmpty()) {
            return "Please provide a message.";
        }
        return "Echo: " + prompt;
    }
}
