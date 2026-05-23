// src/main/java/com/ai/ecommerce/controller/OrderController.java
package com.ai.ecommerce.controller;

import com.ai.ecommerce.entity.CustomerOrder;
import com.ai.ecommerce.service.OrderService;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/orders")
public class OrderController {
    private final OrderService svc;

    public OrderController(OrderService svc) { this.svc = svc; }

    @GetMapping
    public List<CustomerOrder> all() { return svc.findAll(); }

    @GetMapping("/{id}")
    public ResponseEntity<CustomerOrder> get(@PathVariable Long id) {
        return svc.findById(id).map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<CustomerOrder> create(@RequestBody CustomerOrder o) {
        return new ResponseEntity<>(svc.save(o), HttpStatus.CREATED);
    }

    @PutMapping("/{id}")
    public ResponseEntity<CustomerOrder> update(@PathVariable Long id, @RequestBody CustomerOrder o) {
        return ResponseEntity.ok(svc.update(id, o));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        svc.delete(id);
        return ResponseEntity.noContent().build();
    }
}
