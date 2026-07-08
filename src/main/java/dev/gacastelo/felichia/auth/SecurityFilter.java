package dev.gacastelo.felichia.auth;

import com.auth0.jwt.exceptions.JWTVerificationException;
import dev.gacastelo.felichia.exceptions.ErroApi;
import dev.gacastelo.felichia.exceptions.NaoEncontradoException;
import dev.gacastelo.felichia.user.entity.User;
import dev.gacastelo.felichia.user.repository.UserRepository;
import dev.gacastelo.felichia.auth.userCustomer.UserCustomDetails;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.jspecify.annotations.NonNull;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;
import tools.jackson.databind.ObjectMapper;

import java.io.IOException;
import java.time.Instant;
import java.util.List;
import java.util.UUID;

@Component
public class SecurityFilter extends OncePerRequestFilter {

    private final TokenService tokenService;
    private final UserRepository userRepository;

    public SecurityFilter(TokenService tokenService, UserRepository userRepository) {
        this.tokenService = tokenService;
        this.userRepository = userRepository;
    }


    @Override
    protected void doFilterInternal(@NonNull HttpServletRequest request, @NonNull HttpServletResponse response, @NonNull FilterChain filterChain)
            throws ServletException, IOException {
        try {
            var token = this.recoverToken(request);

            if (token != null) {
                var userId = tokenService.validateToken(token);
                if (userId != null) {
                    User user = userRepository.findById(UUID.fromString(userId)).orElseThrow(() -> new NaoEncontradoException("Usuário Inválido!"));
                    UserCustomDetails userDetails = new UserCustomDetails(user);
                    var authentication = new UsernamePasswordAuthenticationToken(userDetails, null, userDetails.getAuthorities());
                    SecurityContextHolder.getContext().setAuthentication(authentication);
                }
            }

            filterChain.doFilter(request, response);
        } catch (JWTVerificationException ex) {
            response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
            response.setContentType("application/json");

            ErroApi erroApi = new ErroApi(
                    Instant.now(),
                    500,
                    "Erro Interno",
                    ex.getMessage(),
                    request.getRequestURI(),
                    List.of()
            );

            new ObjectMapper().writeValue(response.getWriter(), erroApi);
        }
    }

    private String recoverToken(HttpServletRequest request) {
        var authHeader = request.getHeader("Authorization");
        if (authHeader == null || authHeader.isBlank() || !authHeader.startsWith("Bearer ")) {
            return null;
        }
        return authHeader.replace("Bearer ", "").trim();
    }
}