package dev.gacastelo.felichia.vault;

import dev.gacastelo.felichia.vault.dto.VaultDTO;
import dev.gacastelo.felichia.vault.entity.Vault;

public class VaultMapper {

    public static VaultDTO mapToDto(Vault vault) {
        return VaultDTO.builder()
                .id(vault.getId())
                .vaultData(vault.getVaultData())
                .version(vault.getVersion())
                .build();
    }
}
