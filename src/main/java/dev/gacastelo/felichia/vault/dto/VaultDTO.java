package dev.gacastelo.felichia.vault.dto;

import lombok.Builder;

import java.util.UUID;
@Builder
public record VaultDTO(
    UUID id,
    byte[] vaultData,
    Integer version
) {
}
