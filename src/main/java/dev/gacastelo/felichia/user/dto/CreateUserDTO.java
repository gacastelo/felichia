package dev.gacastelo.felichia.user.dto;

import lombok.Builder;

@Builder
public record CreateUserDTO(
        String name,
        String email,
        String passwordHash
) {
}
