package com.example.repository

import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import kotlin.test.assertTrue

@DataJpaTest(properties = [
    "spring.datasource.url=jdbc:h2:mem:testdb",
    "spring.jpa.hibernate.ddl-auto=create-drop"
])
class EntityRepositoryTest(
    @Autowired
    private val entityRepository: EntityRepository
) {
    @Test
    fun testFindByName() {
        val entity = Entity(name = "Test Entity")
        entityRepository.save(entity)

        val foundEntity = entityRepository.findByName("Test Entity")
        assertTrue(foundEntity.isPresent)
        assertTrue(foundEntity.get().name == "Test Entity")
    }

    @Test
    fun testFindByNameWithPreloadedData() {
        // Add preloaded data test if needed
    }
}
