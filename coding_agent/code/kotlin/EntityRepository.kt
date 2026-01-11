package com.example.repository

import com.example.entity.Entity
import org.springframework.data.jpa.repository.JpaRepository

interface EntityRepository : JpaRepository<Entity, Long>