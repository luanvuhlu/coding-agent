package com.example.security.jwt

import io.jsonwebtoken.*
import io.jsonwebtoken.security.Keys
import org.springframework.beans.factory.annotation.Value
import org.springframework.security.core.userdetails.UserDetails
import org.springframework.stereotype.Service
import javax.crypto.SecretKey
import java.util.Date

@Service
class JwtService {

    @Value("${'$'}{jwt.secret}")
    lateinit var secret: String

    @Value("${'$'}{jwt.expiration:3600000}")
    var expiration: Long = 3600000

    fun generateToken(userDetails: UserDetails): String {
        val claims = HashMap<String, Any>()
        return createToken(claims, userDetails.username)
    }

    private fun createToken(claims: Map<String, Any>, subject: String): String {
        val now = Date()
        val expiryDate = Date(now.time + expiration)

        return Jwts.builder()
            .setClaims(claims)
            .setSubject(subject)
            .setIssuedAt(now)
            .setExpiration(expiryDate)
            .signWith(getSigningKey())
            .compact()
    }

    fun validateToken(token: String, userDetails: UserDetails): Boolean {
        val username = extractUsername(token)
        return username == userDetails.username && !isTokenExpired(token)
    }

    fun extractUsername(token: String): String {
        return extractClaim(token, Claims::getSubject)
    }

    private fun getSigningKey(): SecretKey {
        return Keys.hmacShaKeyFor(secret.toByteArray())
    }

    private fun isTokenExpired(token: String): Boolean {
        return extractExpiration(token).before(Date())
    }

    private fun extractExpiration(token: String): Date {
        return extractClaim(token, Claims::getExpiration)
    }

    private fun <T> extractClaim(token: String, claimsResolver: (Claims) -> T): T {
        val claims = extractAllClaims(token)
        return claimsResolver(claims)
    }

    private fun extractAllClaims(token: String): Claims {
        return Jwts.parserBuilder()
            .setSigningKey(getSigningKey())
            .build()
            .parseClaimsJws(token)
            .body
    }
}
