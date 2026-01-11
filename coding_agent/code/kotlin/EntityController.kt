package com.example.comtroller

import com.example.entity.Entity
import com.example.service.EntityService
import jakarta.validation.Valid
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/entities")
class EntityController(private val entityService: EntityService) {

    @GetMapping
    fun getAllEntities(page: Int, size: Int): List<EntityResponse> {
        val entities = entityService.getAllEntities(page, size)
        val entityResponses = entities.content.map { EntityResponse.fromEntity(it) }
        val pageImpl = PageImpl(entityResponses, entities.pageable, entities.totalElements)
        return ResponseEntity.ok(pageImpl)
    }

    @GetMapping("/{id}")
    fun getEntityById(@PathVariable id: Long): ResponseEntity<EntityResponse> {
        val entity = entityService.getEntityById(id)
        return if (entity != null) {
            ResponseEntity.ok(EntityResponse.fromEntity(entity))
        } else {
            ResponseEntity.notFound().build()
        }
    }
    @PostMapping
    fun createEntity(@Valid @RequestBody entity: EntityCreateRequest): EntityResponse {
        return EntityResponse.fromEntity(entityService.createEntity(entity))
    }

    @PutMapping("/{id}")
    fun updateEntity(@PathVariable id: Long, @Valid @RequestBody updatedEntity:
        Entity): ResponseEntity<EntityResponse> {
        val entity = entityService.updateEntity(id, updatedEntity)
        return if (entity != null) {
            ResponseEntity.ok(EntityResponse.fromEntity(entity))
        } else {
            ResponseEntity.notFound().build()
        }
    }
    @DeleteMapping("/{id}")
    fun deleteEntity(@PathVariable id: Long): ResponseEntity<Void> {
        return if (entityService.deleteEntity(id)) {
            ResponseEntity.noContent().build()
        } else {
            ResponseEntity.notFound().build()
        }
    }
}