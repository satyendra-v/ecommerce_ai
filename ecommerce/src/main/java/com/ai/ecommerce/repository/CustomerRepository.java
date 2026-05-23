// src/main/java/com/ai/ecommerce/repository/CustomerRepository.java
package com.ai.ecommerce.repository;

import com.ai.ecommerce.entity.Customer;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CustomerRepository extends JpaRepository<Customer, Long> {
}
