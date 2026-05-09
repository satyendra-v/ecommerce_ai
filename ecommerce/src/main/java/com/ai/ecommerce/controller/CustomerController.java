package com.ai.ecommerce.controller;

import com.ai.ecommerce.entity.Customer;
import com.ai.ecommerce.service.CustomerService;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/customers")
public class CustomerController {
    private final CustomerService svc;

    public CustomerController(CustomerService svc) { this.svc = svc; }

    @GetMapping
    public List<Customer> all() { return svc.findAll(); }

    @GetMapping("/{id}")
    public ResponseEntity<Customer> get(@PathVariable Long id) {
        return svc.findById(id).map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<Customer> create(@RequestBody Customer c) {
        return new ResponseEntity<>(svc.save(c), HttpStatus.CREATED);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Customer> update(@PathVariable Long id, @RequestBody Customer c) {
        return ResponseEntity.ok(svc.update(id, c));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        svc.delete(id);
        return ResponseEntity.noContent().build();
    }
}
