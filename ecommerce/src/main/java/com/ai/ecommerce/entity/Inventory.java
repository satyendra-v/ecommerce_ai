// src/main/java/com/ai/ecommerce/entity/Inventory.java
package com.ai.ecommerce.entity;

import jakarta.persistence.*;
import lombok.Data;

@Entity
@Table(name = "inventory")
@Data
public class Inventory {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long inventoryId;

    // foreign key as simple Long
    private Long productId;

    private Integer quantity;
    private String location;
}
