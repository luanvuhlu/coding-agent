package com.example.service

import org.junit.jupiter.api.Test
import org.junit.jupiter.api.extension.ExtendWith
import org.mockito.InjectMocks
import org.mockito.Mock
import org.mockito.junit.jupiter.MockitoExtension
import org.mockito.kotlin.whenever
import org.mockito.kotlin.verify
import org.mockito.kotlin.times
import org.mockito.kotlin.mock
import kotlin.test.assertEquals

@ExtendWith(MockitoExtension::class)
class EntityServiceTest {

    @Mock
    lateinit var entityRepository: EntityRepository

    @InjectMocks
    lateinit var entityService: EntityService

    @Test
    fun `getAllEntities should return list`() {
        val mockEntities = listOf(Entity(1L, "Entity1"), Entity(2L, "Entity2"))
        whenever(entityRepository.findAll(org.mockito.kotlin.any())).thenReturn(org.springframework.data.domain.PageImpl(mockEntities))

        val entities = entityService.getAllEntities(0, 10)
        assertEquals(2, entities.content.size)
    }
}
