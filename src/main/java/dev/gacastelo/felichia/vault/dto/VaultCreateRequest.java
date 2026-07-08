package dev.gacastelo.felichia.vault.dto;

import jakarta.validation.constraints.NotNull;

public record VaultCreateRequest(
        @NotNull byte[] vaultData
) {
}
