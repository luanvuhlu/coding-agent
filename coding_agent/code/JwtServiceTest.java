package com.example.security.jwt;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import static org.junit.jupiter.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
class JwtServiceTest {
    
    @InjectMocks
    private JwtService jwtService;
    
    @Test
    void generateToken_ShouldReturnValidToken() {
        var user = User.builder()
            .username("test@example.com")
            .password("password")
            .roles("USER")
            .build();
        
        var token = jwtService.generateToken(user);
        
        assertNotNull(token);
        assertTrue(jwtService.validateToken(token, user));
    }
}