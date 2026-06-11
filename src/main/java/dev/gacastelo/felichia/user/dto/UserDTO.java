package dev.gacastelo.felichia.user.dto;

import lombok.Builder;

import java.util.UUID;

@Builder
public record UserDTO(
    UUID id,
    String name,
    String email,
    boolean emailVerified,
    boolean enabled
){}
