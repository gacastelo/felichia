package dev.gacastelo.felichia.auth;

import dev.gacastelo.felichia.auth.request.CreateUserRequest;
import dev.gacastelo.felichia.auth.request.LoginRequest;
import dev.gacastelo.felichia.user.entity.User;
import dev.gacastelo.felichia.user.service.UserService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/api/auth")
public class AuthController {

    private final UserService userService;
    private final PasswordEncoder passwordEncoder;
    private final TokenService tokenService;

    public AuthController(UserService userService, PasswordEncoder passwordEncoder, TokenService tokenService) {
        this.userService = userService;
        this.passwordEncoder = passwordEncoder;
        this.tokenService = tokenService;
    }

    @PostMapping("/register")
    public ResponseEntity<?> registerUser(@RequestBody CreateUserRequest request) {
        userService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).build();
    }

    @PostMapping("/login")
    public ResponseEntity<String> loginUser(@RequestBody LoginRequest request){
        User user = userService.findByUsername(request.username());

        if(user == null || !passwordEncoder.matches(request.password(), user.getPassword())) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Usuário ou senha inválidos");
        }

        String token = tokenService.gerarToken(user.getId(), user.getUsername());

        return ResponseEntity.ok(token);
    }

    @GetMapping("/test")
    public ResponseEntity<String> test(@AuthenticationPrincipal User user){
        if(user != null){
            return ResponseEntity.ok("Olá " + user.getUsername() + ", seu JWT está Válido!");
        }
        else{
            return ResponseEntity.status(HttpStatus.FORBIDDEN).body("Acesso negado: JWT Inválido ou ausente");
        }
    }
}
