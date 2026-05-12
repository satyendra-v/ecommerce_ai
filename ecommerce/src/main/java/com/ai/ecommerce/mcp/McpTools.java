package com.ai.ecommerce.mcp;

import com.ai.ecommerce.entity.CustomerOrder;
import com.ai.ecommerce.entity.Inventory;
import com.ai.ecommerce.entity.Product;
import com.ai.ecommerce.service.InventoryService;
import com.ai.ecommerce.service.OrderService;
import com.ai.ecommerce.service.ProductService;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Slf4j
@Component
public class McpTools {

    @Autowired
    private ProductService productService;

    @Autowired
    private InventoryService inventoryService;

    @Autowired
    private OrderService orderService;

    // Product Tools
    @Tool(description = """
            Search the product catalog. Check this when a user asks information about products like price, description,
            or wants to find specific products by name, type, or price range.
            """)
    public List<Map<String, Object>> searchProducts(
            @ToolParam(description = "Keyword to search(any name/ price/ date related to products, orders, inventory") String query,
            @ToolParam(description = "Product name(ase insensitive) to search for", required = false) String name,
            @ToolParam(description = "Max price in USD. defaults to none", required = false) Double maxPrice
    ) {
        List<Product> products = productService.findAll();

        System.out.println("Filtering products with query='" + query + "', name='" + name + "', maxPrice=" + maxPrice);

        List<Map<String, Object>> res = products.stream()
                .filter(p -> {
                    String q = query == null ? null : query.toLowerCase();
                    String pname = p.getName() == null ? "" : p.getName().toLowerCase();
                    String pdesc = p.getDescription() == null ? "" : p.getDescription().toLowerCase();
                    boolean matchesQuery = q == null || pname.contains(q) || pdesc.contains(q);
                    boolean matchesName = name == null || pname.contains(name.toLowerCase());
                    boolean matchesPrice = maxPrice == null || p.getPrice().doubleValue() <= maxPrice;
                    return matchesQuery && matchesName && matchesPrice;
                })
                .map(p -> {
                    Map<String, Object> m = new HashMap<>();
                    m.put("id", p.getProductId());
                    m.put("name", p.getName());
                    m.put("description", p.getDescription());
                    m.put("price", p.getPrice());
                    return m;
                })
                .collect(Collectors.toList());

        System.out.println("result : " + res);
        return res;
    }

    @Tool(description = """
    Get stock inventory for a product by its name which first looks up the product to get its ID and then finds inventory.
    Or Get inventory for all products if product name is not provided by listing products names with help of product id from inventory.
    Use when users ask about stock availability.""")
    public Map<String, Object> getInventory(
            @ToolParam(description = "Product name with case insensitive", required = false) String productName,
            @ToolParam(description = "quantity threshold to filter products with low stock, e.g. 5. If provided, returns products with inventory quantity less than or equal to this value.", required = false) Integer lowStockThreshold
    ) {
        if (StringUtils.isNoneBlank(productName)) {
            Product product = productService.getProductByName(productName);
            if(null == product) {
                return Map.of("error", "Product not found for product Name " + productName);
            }

            Inventory inventory = inventoryService.findByProductId(product.getProductId());
            if (inventory == null) {
                return Map.of("error", "Inventory not found for product Name " + productName);
            }

            return Map.of(
                    "inventoryId", inventory.getInventoryId(),
                    "inventoryLocation", inventory.getLocation(),
                    "productId", inventory.getProductId(),
                    "quantity", inventory.getQuantity()
            );
        } else if (lowStockThreshold != null) {
            List<Inventory> lowStockInventories = inventoryService.findAll().stream()
                    .filter(inv -> inv.getQuantity() <= lowStockThreshold)
                    .toList();

            List<Map<String, Object>> lowStockProducts = lowStockInventories.stream()
                    .map(inv -> {

                        Map<String, Object> m = new HashMap<>();
                        Product p = productService.findById(inv.getProductId()).orElse(null);
                        String name = p != null ? p.getName() : "Unknown Product";
                        m.put("productId", inv.getProductId());
                        m.put("productName", name);
                        m.put("quantity", inv.getQuantity());
                        return m;
                    }).toList();

            return Map.of("lowStockProducts", lowStockProducts);
        } else {
            return Map.of("error", "Please provide either productName or lowStockThreshold to get inventory information.");
        }

    }

    // Order Tools
    @Tool(description = """
        Look up an order by its ID. Returns status, items, shipping info.
        Use when customers ask about their order status or delivery.
        """)
    public Map<String, Object> getOrder(
            @ToolParam(description = "Order ID long e.g. 12345") Long orderId
    ) {
        CustomerOrder order = orderService.findById(orderId).orElse(null);
        if (order == null) {
            return Map.of("error", "Order not found for ID " + orderId);
        }
        return Map.of(
                "orderId", order.getOrderId(),
                "status", order.getOrderStatus(),
                "customerId", order.getCustomerId(),
                "productId", order.getProductId(),
                "quantity", order.getQuantity(),
                "totalPrice", order.getTotalPrice(),
                "orderDate", order.getOrderDate()
        );
    }

    /*@Tool(description = """
        Create a support ticket for an issue that requires human follow-up.
        Use for complaints, refund requests, or issues the AI cannot resolve.
        """)
    public Map<String, Object> createSupportTicket(
            @ToolParam(description = "Customer email address") String customerEmail,
            @ToolParam(description = "Subject/title of the issue") String subject,
            @ToolParam(description = "Detailed description of the issue") String description,
            @ToolParam(description = "Priority: low, medium, high, or critical") String priority
    ) {
        String ticketId = "TKT-" + System.currentTimeMillis();
        return Map.of(
                "ticket_id", ticketId,
                "status", "created",
                "message", "Support ticket " + ticketId + " created with " + priority + " priority."
        );
    }*/

    /*@Tool(description = """
        Process a refund for an order. Requires order ID and reason.
        Returns the refund reference number and expected processing time.
        """)
    public Map<String, Object> processRefund(
            @ToolParam(description = "Order ID to refund") String orderId,
            @ToolParam(description = "Reason for refund") String reason
    ) {
        return Map.of(
                "refund_id", "REF-" + orderId,
                "status", "approved",
                "amount_usd", 749.0,
                "processing_days", 5,
                "message", "Refund approved. Expect credit within 5 business days."
        );
    }*/

    // Analytics Tools
    @Tool(description = "Get sales metrics for a date range. Returns revenue, orders, and top products.")
    public Map<String, Object> getSalesMetrics(
            @ToolParam(description = "Start date YYYY-MM-DD") String startDate,
            @ToolParam(description = "End date YYYY-MM-DD") String endDate
    ) {
        return Map.of(
                "startDate", startDate,
                "endDate", endDate,
                "totalRevenueUsd", 12345.67,
                "totalOrders", 89,
                "topProducts", List.of(
                        Map.of("productId", 1, "name", "Widget A", "unitsSold", 50, "revenueUsd", 4999.50),
                        Map.of("productId", 2, "name", "Widget B", "unitsSold", 30, "revenueUsd", 2999.70)
                )
        );
    }
}
