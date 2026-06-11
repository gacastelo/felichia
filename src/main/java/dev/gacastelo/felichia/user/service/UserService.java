package dev.gacastelo.felichia.user.service;

import dev.gacastelo.felichia.exceptions.NaoEncontradoException;
import dev.gacastelo.felichia.user.UserMapper;
import dev.gacastelo.felichia.user.dto.CreateUserDTO;
import dev.gacastelo.felichia.user.dto.UpdateUserDTO;
import dev.gacastelo.felichia.user.dto.UserDTO;
import dev.gacastelo.felichia.user.entity.User;
import dev.gacastelo.felichia.user.repository.UserRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

@Service
public class UserService {

    private final UserRepository userRepository;


    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public List<UserDTO> findAllUsers(){
        return userRepository.findAll().stream().map(UserMapper::toDTO).toList();
    }

    public UserDTO findById(UUID id) {
        User user = userRepository.findById(id).orElseThrow(() -> new NaoEncontradoException("Usuário não encontrado: " + id));
        return UserMapper.toDTO(user);
    }

    public UserDTO create(CreateUserDTO dto) {
        User user = User.builder()
                .id(UUID.randomUUID())
                .name(dto.name())
                .email(dto.email())
                .passwordHash(dto.passwordHash())
                .build();
        User response = userRepository.save(user);
        return UserMapper.toDTO(response);
    }

    public UserDTO update(UUID id, UpdateUserDTO dto) {
        User u = userRepository.findById(id).orElseThrow(() -> new NaoEncontradoException("Usuário não encontrado: " + id));

        u.setName(dto.name().isEmpty() ? u.getName() : dto.name());
        u.setEmail(dto.email().isEmpty() ? u.getEmail() : dto.email());
        u.setPasswordHash(dto.passwordHash().isEmpty() ? u.getPasswordHash() : dto.passwordHash());

        u = userRepository.save(u);
        return UserMapper.toDTO(u);
    }

    public void disable(UUID id) {
        User u = userRepository.findById(id).orElseThrow(() -> new NaoEncontradoException("Usuário não encontrado: " + id));
        u.setEnabled(false); //TODO: Schema que acada x periodo deleta todos os enabled false
        userRepository.save(u);
    }


}
