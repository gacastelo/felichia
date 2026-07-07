package dev.gacastelo.felichia.user.dto;

import lombok.Builder;

@Builder
public record UpdateUserRequest(
        String name,
        String email,
        String password
) {
}
