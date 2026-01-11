package com.example.controller;

import com.example.entity.Entity;
import com.example.service.EntityService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import com.example.response.EntityResponse;
import com.example.request.EntityCreateRequest;


@RestController
@RequestMapping("/api/entities")
public class EntityController {
    private final EntityService entityService;

    public EntityController(EntityService entityService) {
        this.entityService = entityService;
    }

    @GetMapping
    public ResponseEntity<Page<EntityResponse>> getAllEntities(
        int page,
        int size
    ) {
        var entities = entityService.getAllEntities(page, size);
        var EntityResponses = entities.getContent().stream()
                                             .map(EntityResponse::fromEntity)
                                             .toList();
        var pageImpl = new PageImpl<>(EntityResponses, entities.getPageable(), entities.getTotalElements());
        return ResponseEntity.ok(pageImpl);
    }

    @GetMapping("/{id}")
    public ResponseEntity<EntityResponse> getEntityById(@PathVariable Long id) {
        return entityService.getEntityById(id)
                .map(entity -> ResponseEntity.ok(EntityResponse.fromEntity(entity)))
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<EntityResponse> createEntity(@RequestBody EntityCreateRequest createRequest) {
        var createdEntity = entityService.createEntity(createRequest);
        return ResponseEntity.ok(EntityResponse.fromEntity(createdEntity));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteEntity(@PathVariable Long id) {
        entityService.deleteEntity(id);
        return ResponseEntity.noContent().build();
    }
}
