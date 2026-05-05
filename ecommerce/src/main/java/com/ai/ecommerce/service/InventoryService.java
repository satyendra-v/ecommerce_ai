// src/main/java/com/ai/ecommerce/service/InventoryService.java
package com.ai.ecommerce.service;

import com.ai.ecommerce.entity.Inventory;
import com.ai.ecommerce.repository.InventoryRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class InventoryService {
    private final InventoryRepository repo;

    public InventoryService(InventoryRepository repo) { this.repo = repo; }

    public List<Inventory> findAll() { return repo.findAll(); }
    public Optional<Inventory> findById(Long id) { return repo.findById(id); }
    public Inventory save(Inventory i) { return repo.save(i); }
    public Inventory update(Long id, Inventory i) {
        i.setInventoryId(id);
        return repo.save(i);
    }
    public void delete(Long id) { repo.deleteById(id); }
}
