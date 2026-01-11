package com.example.request;

import jakarta.validation.constraints.NotBlank;
data class EntityCreateRequest(
    @field:NotBlank
    val name: String,
    val description: String
)