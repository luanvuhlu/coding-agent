package com.example.service

import com.example.entity.Entity
import com.example.repository.EntityRepository
import org.springframework.stereotype.Service
import org.springframework.data.domain.Page
import org.springframework.data.domain.PageRequest

@Service
class EntityService(private val entityRepository: EntityRepository) {

    fun getAllEntities(page: Int, size: Int): Page<Entity> {
        return entityRepository.findAll(PageRequest.of(page, size))
    }

    fun getEntityById(id: Long): Entity? = entityRepository.findById(id).orElse(null)

    fun createEntity(entity: Entity): Entity = entityRepository.save(entity)

    fun deleteEntity(id: Long) = try {
        entityRepository.deleteById(id)
        true
    } catch (e: Exception) {
        false
    }
}
