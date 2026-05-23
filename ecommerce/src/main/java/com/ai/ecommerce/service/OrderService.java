// src/main/java/com/ai/ecommerce/service/OrderService.java
package com.ai.ecommerce.service;

import com.ai.ecommerce.entity.CustomerOrder;
import com.ai.ecommerce.repository.OrderRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class OrderService {
    private final OrderRepository repo;

    public OrderService(OrderRepository repo) { this.repo = repo; }

    public List<CustomerOrder> findAll() { return repo.findAll(); }
    public Optional<CustomerOrder> findById(Long id) { return repo.findById(id); }
    public CustomerOrder save(CustomerOrder o) { return repo.save(o); }
    public CustomerOrder update(Long id, CustomerOrder o) {
        o.setOrderId(id);
        return repo.save(o);
    }
    public void delete(Long id) { repo.deleteById(id); }
}
