package com.example.response;

import com.example.entity.Entity;

public record EntityResponse(Long id, String name) {
    public static EntityResponse fromEntity(Entity entity) {
        return new EntityResponse(entity.getId(), entity.getName());
    }
}
