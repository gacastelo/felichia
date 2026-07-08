package dev.gacastelo.felichia.user.controller;

import dev.gacastelo.felichia.auth.userCustomer.UserCustomDetails;
import dev.gacastelo.felichia.user.UserMapper;
import dev.gacastelo.felichia.user.dto.UpdateUserRequest;
import dev.gacastelo.felichia.user.dto.UserDTO;
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
    public ResponseEntity<UserDTO> getUser(@AuthenticationPrincipal UserCustomDetails user) {
        return ResponseEntity.ok(UserMapper.toDTO(user));
    }

    @PatchMapping
    public UserDTO updateUser(@AuthenticationPrincipal UserCustomDetails user, @RequestBody UpdateUserRequest updateUserRequest) {
        return userService.update(user.getId(), updateUserRequest);
    }

    @DeleteMapping
    public ResponseEntity<?> deleteUser(@AuthenticationPrincipal UserCustomDetails user) {
        userService.delete(user.getId());
        return ResponseEntity.ok().build();
    }

}
