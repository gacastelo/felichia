package dev.gacastelo.felichia.auth.request;

import lombok.Builder;

@Builder
public record CreateUserRequest(
        String username,
        String email,
        String password
) {
}
