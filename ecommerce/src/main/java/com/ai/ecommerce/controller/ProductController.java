// src/main/java/com/ai/ecommerce/controller/ProductController.java
package com.ai.ecommerce.controller;

import com.ai.ecommerce.entity.Product;
import com.ai.ecommerce.service.ProductService;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/products")
public class ProductController {
    private final ProductService svc;

    public ProductController(ProductService svc) { this.svc = svc; }

    @GetMapping
    public List<Product> all(
            @RequestParam(required = false, value = "query") String query,
            @RequestParam(required = false, value="name") String name,
            @RequestParam(required = false, value = "max_price") Double maxPrice) {

        List<Product> products = svc.findAll();

        System.out.println("Filtering products with query='" + query + "', name='" + name + "', maxPrice=" + maxPrice);

        List<Product> res = products.stream()
                .filter(p -> query == null || p.getName().toLowerCase().contains(query.toLowerCase()) || p.getDescription().toLowerCase().contains(query.toLowerCase()))
                .filter(p -> name == null || p.getName().toLowerCase().contains(name.toLowerCase()))
                .filter(p -> maxPrice == null || p.getPrice().doubleValue() <= maxPrice)
                .toList();

        System.out.println("result : "+res);
        return res;
    }

    @GetMapping("/{id}")
    public ResponseEntity<Product> get(@PathVariable Long id) {
        return svc.findById(id).map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<Product> create(@RequestBody Product p) {
        return new ResponseEntity<>(svc.save(p), HttpStatus.CREATED);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Product> update(@PathVariable Long id, @RequestBody Product p) {
        return ResponseEntity.ok(svc.update(id, p));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        svc.delete(id);
        return ResponseEntity.noContent().build();
    }
}
