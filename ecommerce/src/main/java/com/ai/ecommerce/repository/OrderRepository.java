// src/main/java/com/ai/ecommerce/repository/OrderRepository.java
package com.ai.ecommerce.repository;

import com.ai.ecommerce.entity.CustomerOrder;
import org.springframework.data.jpa.repository.JpaRepository;

public interface OrderRepository extends JpaRepository<CustomerOrder, Long> {
}
