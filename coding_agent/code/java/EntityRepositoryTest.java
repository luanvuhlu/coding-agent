package com.example.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import com.example.entity.Entity;
import java.util.Optional;
import org.junit.jupiter.api.Test;

@DataJpaTest(properties = {
    "spring.datasource.url=jdbc:h2:mem:testdb",
    "spring.jpa.hibernate.ddl-auto=create-drop"
})
public class EntityRepositoryTest {
    private final EntityRepository entityRepository;

    public EntityRepositoryTest(EntityRepository entityRepository) {
        this.entityRepository = entityRepository;
    }

    @Test
    void testFindByName() {
        var entity = new Entity();
        entity.setName("Test Entity");
        entityRepository.save(entity);

        var foundEntity = entityRepository.findByName("Test Entity");
        assert(foundEntity.isPresent());
        assert(foundEntity.get().getName().equals("Test Entity"));
    }

    @Sql({"INSERT INTO entity (id, name) VALUES (1, 'Entity One');",
          "INSERT INTO entity (id, name) VALUES (2, 'Entity Two');"})
    @Test
    void testFindByName_WithPreloadedData() {
        var foundEntity = entityRepository.findByName("Entity One");
        assert(foundEntity.isPresent());
        assert(foundEntity.get().getName().equals("Entity One"));
    }
}