package dev.gacastelo.felichia.vault.dto;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

public record VaultUpdateRequest(
        @NotNull byte[] vaultData,
        @NotNull byte[] nonce,
        @NotNull byte[] salt,
        @NotNull @Positive Integer version
) {
}
