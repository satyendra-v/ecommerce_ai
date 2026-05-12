package com.ai.ecommerce.mcp.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import com.ai.ecommerce.mcp.McpTools;

@Configuration
public class McpConfig {

    @Bean
    public ToolCallbackProvider toolCallBacks(McpTools mcpTools) {
        // existing code...
    }
}
