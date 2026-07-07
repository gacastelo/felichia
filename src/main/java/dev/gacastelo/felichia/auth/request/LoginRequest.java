package dev.gacastelo.felichia.auth.request;

import lombok.Builder;

@Builder
public record LoginRequest(
        String username,
        String password
) {
}
