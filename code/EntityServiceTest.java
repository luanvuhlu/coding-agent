package com.example.service;

import com.example.entity.Entity;
import com.example.repository.EntityRepository;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
public class EntityServiceTest {

    @Mock
    private EntityRepository entityRepository;

    @InjectMocks
    private EntityService entityService;

    @Test
    void getAllEntities_ShouldReturnListOfEntities() {
        var mockEntities = List.of(new Entity(1L, "Entity1"), new Entity(2L, "Entity2"));
        when(entityRepository.findAll()).thenReturn(mockEntities);

        var entities = entityService.getAllEntities();

        assertEquals(2, entities.size());
        assertEquals("Entity1", entities.get(0).getName());
    }
}
