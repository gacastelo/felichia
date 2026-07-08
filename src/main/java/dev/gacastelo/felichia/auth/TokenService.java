package dev.gacastelo.felichia.auth;

import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.exceptions.JWTCreationException;
import com.auth0.jwt.exceptions.JWTVerificationException;
import dev.gacastelo.felichia.config.Config;
import org.springframework.stereotype.Service;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.UUID;

@Service
public class TokenService {

    public String gerarToken(UUID id, String username) {
        try {
            Algorithm algorithm = Algorithm.HMAC256(Config.JWT_SECRET);
            return JWT.create()
                    .withIssuer("SecurityStudy")
                    .withSubject(id.toString())
                    .withClaim("username", username)
                    .withExpiresAt(dataExpiracao())
                    .sign(algorithm);
        } catch (JWTCreationException exception){
            throw new RuntimeException(exception);
        }
    }

    private Instant dataExpiracao() {
        return LocalDateTime.now().plusMinutes(Config.minutesToExpireJwtToken).toInstant(ZoneOffset.of("-03:00"));
    }

    public String validateToken(String token) {
        try {
            Algorithm algorithm = Algorithm.HMAC256(Config.JWT_SECRET);
            return JWT.require(algorithm)
                    .withIssuer("SecurityStudy")
                    .build()
                    .verify(token)
                    .getSubject();
        } catch (JWTVerificationException exception) {
            throw new JWTVerificationException(exception.getMessage());
        }
    }

}
