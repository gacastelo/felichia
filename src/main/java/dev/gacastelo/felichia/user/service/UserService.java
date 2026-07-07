package dev.gacastelo.felichia.user.service;

import dev.gacastelo.felichia.exceptions.NaoEncontradoException;
import dev.gacastelo.felichia.user.UserMapper;
import dev.gacastelo.felichia.auth.request.CreateUserRequest;
import dev.gacastelo.felichia.user.dto.UpdateUserRequest;
import dev.gacastelo.felichia.user.dto.UserDTO;
import dev.gacastelo.felichia.user.entity.User;
import dev.gacastelo.felichia.user.repository.UserRepository;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

@Service
public class UserService {

    private final UserRepository userRepository;

    private final PasswordEncoder passwordEncoder;


    public UserService(UserRepository userRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    public List<UserDTO> findAllUsers(){
        return userRepository.findAll().stream().map(UserMapper::toDTO).toList();
    }

    public UserDTO findById(UUID id) {
        User user = userRepository.findById(id).orElseThrow(() -> new NaoEncontradoException("Usuário não encontrado: " + id));
        return UserMapper.toDTO(user);
    }

    public UserDTO create(CreateUserRequest request) {
        var senhaCriptografada = passwordEncoder.encode(request.password());
        User user = User.builder()
                .id(UUID.randomUUID())
                .username(request.username())
                .email(request.email())
                .password(senhaCriptografada)
                .build();
        User response = userRepository.save(user);
        return UserMapper.toDTO(response);
    }

    public UserDTO update(UUID id, UpdateUserRequest request) {
        User u = userRepository.findById(id).orElseThrow(() -> new NaoEncontradoException("Usuário não encontrado: " + id));

        if (!request.name().isEmpty()){
            u.setUsername(request.name());
        }

        if (!request.email().isEmpty()){
            u.setEmail(request.email());
        }

        if (!request.password().isEmpty()) {
            u.setPassword(passwordEncoder.encode(request.password()));
        }
        u = userRepository.save(u);
        return UserMapper.toDTO(u);
    }

    public void delete(UUID id) {
        userRepository.deleteById(id);
    }

    public User findByUsername(String username) {
        return userRepository.findByUsername(username).orElseThrow(() -> new NaoEncontradoException("Usuário não encontrado: " + username));
    }


}
