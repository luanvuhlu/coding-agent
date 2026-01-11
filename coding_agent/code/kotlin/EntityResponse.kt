package com.example.response;

import com.example.entity.Entity
data class EntityResponse(
    val id: Long,
    val name: String,
    val description: String
) {
    companion object {
        fun fromEntity(entity: Entity): EntityResponse {
            return EntityResponse(
                id = entity.id,
                name = entity.name,
                description = entity.description
            )
        }
    }
}