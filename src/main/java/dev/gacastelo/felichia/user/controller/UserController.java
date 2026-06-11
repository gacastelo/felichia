package dev.gacastelo.felichia.user.controller;

import dev.gacastelo.felichia.user.dto.UpdateUserDTO;
import dev.gacastelo.felichia.user.dto.UserDTO;
import dev.gacastelo.felichia.user.service.UserService;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping
    public List<UserDTO> getUsers() {
        return userService.findAllUsers();
    }


    @PatchMapping("/{id}")
    public UserDTO updateUser(@PathVariable UUID id, @RequestBody UpdateUserDTO updateUserDTO) {
        return userService.update(id, updateUserDTO);
    }

    @DeleteMapping("/{id}")
    public void deleteUser(@PathVariable UUID id) {
        userService.disable(id);
    }
}
