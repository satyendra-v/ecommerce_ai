// src/main/java/com/ai/ecommerce/service/ProductService.java
package com.ai.ecommerce.service;

import com.ai.ecommerce.entity.Product;
import com.ai.ecommerce.repository.ProductRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class ProductService {
    private final ProductRepository repo;

    public ProductService(ProductRepository repo) { this.repo = repo; }

    public List<Product> findAll() { return repo.findAll(); }
    public Optional<Product> findById(Long id) { return repo.findById(id); }
    public Product save(Product p) { return repo.save(p); }
    public Product update(Long id, Product p) {
        p.setProductId(id);
        return repo.save(p);
    }
    public void delete(Long id) { repo.deleteById(id); }

    public Product getProductByName(String productName) {
        return repo.getProductByName(productName);
    }
}
