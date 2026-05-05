// src/main/java/com/ai/ecommerce/repository/InventoryRepository.java
package com.ai.ecommerce.repository;

import com.ai.ecommerce.entity.Inventory;
import org.springframework.data.jpa.repository.JpaRepository;

public interface InventoryRepository extends JpaRepository<Inventory, Long> {
}
