package dev.gacastelo.felichia.user.controller;

import dev.gacastelo.felichia.user.UserMapper;
import dev.gacastelo.felichia.user.dto.UpdateUserRequest;
import dev.gacastelo.felichia.user.dto.UserDTO;
import dev.gacastelo.felichia.user.entity.User;
import dev.gacastelo.felichia.user.service.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/users/me")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping
    public ResponseEntity<UserDTO> getUser(@AuthenticationPrincipal User user) {
        return ResponseEntity.ok(UserMapper.toDTO(user));
    }

    @PatchMapping
    public UserDTO updateUser(@AuthenticationPrincipal User user, @RequestBody UpdateUserRequest updateUserRequest) {
        return userService.update(user.getId(), updateUserRequest);
    }

    @DeleteMapping
    public ResponseEntity<?> deleteUser(@AuthenticationPrincipal User user) {
        userService.delete(user.getId());
        return ResponseEntity.ok().build();
    }

}
