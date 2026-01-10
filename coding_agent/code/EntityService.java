package com.example.service;

import com.example.entity.Entity;
import com.example.repository.EntityRepository;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Optional;
import org.springframework.data.domain.Page;

@Service
public class EntityService {
    private final EntityRepository entityRepository;

    public EntityService(EntityRepository entityRepository) {
        this.entityRepository = entityRepository;
    }

    public Page<Entity> getAllEntities(int page, int size) {
        return entityRepository.findAll(PageRequest.of(page, size));
    }

    public Optional<Entity> getEntityById(Long id) {
        return entityRepository.findById(id);
    }

    public Entity createEntity(Entity entity) {
        return entityRepository.save(entity);
    }

    public void deleteEntity(Long id) {
        entityRepository.deleteById(id);
    }
}
