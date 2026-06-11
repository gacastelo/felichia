package dev.gacastelo.felichia.user;

import dev.gacastelo.felichia.user.dto.UserDTO;
import dev.gacastelo.felichia.user.entity.User;
import org.springframework.stereotype.Component;

@Component
public class UserMapper {

    public static UserDTO toDTO(User user) {
        return UserDTO.builder()
                .id(user.getId())
                .name(user.getName())
                .email(user.getEmail())
                .emailVerified(user.isEmailVerified())
                .enabled(user.isEnabled())
                .build();
    }
}
