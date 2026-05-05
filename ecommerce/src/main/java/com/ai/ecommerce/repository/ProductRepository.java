// src/main/java/com/ai/ecommerce/repository/ProductRepository.java
package com.ai.ecommerce.repository;

import com.ai.ecommerce.entity.Product;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ProductRepository extends JpaRepository<Product, Long> {
}
