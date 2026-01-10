package com.example.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.example.entity.Entity;
import java.util.Optional;
public interface EntityRepository extends JpaRepository<Entity, Long> {
    Optional<Entity> findByName(String name);
}
