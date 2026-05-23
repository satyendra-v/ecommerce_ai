// src/main/java/com/ai/ecommerce/controller/InventoryController.java
package com.ai.ecommerce.controller;

import com.ai.ecommerce.entity.Inventory;
import com.ai.ecommerce.service.InventoryService;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/inventories")
public class InventoryController {
    private final InventoryService svc;

    public InventoryController(InventoryService svc) { this.svc = svc; }

    @GetMapping
    public List<Inventory> all() { return svc.findAll(); }

    @GetMapping("/{id}")
    public ResponseEntity<Inventory> get(@PathVariable Long id) {
        return svc.findById(id).map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<Inventory> create(@RequestBody Inventory i) {
        return new ResponseEntity<>(svc.save(i), HttpStatus.CREATED);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Inventory> update(@PathVariable Long id, @RequestBody Inventory i) {
        return ResponseEntity.ok(svc.update(id, i));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        svc.delete(id);
        return ResponseEntity.noContent().build();
    }
}
