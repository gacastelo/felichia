package dev.gacastelo.felichia.user.dto;

import lombok.Builder;

@Builder
public record UpdateUserDTO(
        String name,
        String email,
        String passwordHash
) {
}
