// src/main/java/com/ai/ecommerce/entity/CustomerOrder.java
package com.ai.ecommerce.entity;

import jakarta.persistence.*;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "customer_order")
@Data
public class CustomerOrder {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long orderId;

    // foreign keys as simple Longs
    private Long customerId;
    private Long productId;

    private Integer quantity;
    private BigDecimal totalPrice;
    private LocalDateTime orderDate;
}
