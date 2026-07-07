package dev.gacastelo.felichia.vault.controller;


import dev.gacastelo.felichia.user.entity.User;
import dev.gacastelo.felichia.vault.VaultMapper;
import dev.gacastelo.felichia.vault.dto.VaultDTO;
import dev.gacastelo.felichia.vault.dto.VaultUpdateRequest;
import dev.gacastelo.felichia.vault.entity.Vault;
import dev.gacastelo.felichia.vault.service.VaultService;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;


@RestController
@RequestMapping("/api/vaults")
public class VaultController {

    private final VaultService vaultService;

    public VaultController(VaultService vaultService) {
        this.vaultService = vaultService;
    }

    @GetMapping
    public ResponseEntity<VaultDTO> getVault(@AuthenticationPrincipal User user) {
        return ResponseEntity.ok(vaultService.getMyVault(user));
    }

    @PostMapping
    public ResponseEntity<VaultDTO> createVault(@AuthenticationPrincipal User user){
        Vault v = vaultService.create(user);
        return ResponseEntity.ok(VaultMapper.mapToDto(v));
    }

    @PutMapping
    public ResponseEntity<VaultDTO> updateVault(@AuthenticationPrincipal User user, VaultUpdateRequest request) {
        return ResponseEntity.ok(vaultService.update(user, request));
    }

    @DeleteMapping
    public ResponseEntity<Void> deleteVault(@AuthenticationPrincipal User user) {
        vaultService.disable(user);
        return ResponseEntity.ok().build();
    }

    @PostMapping("{vaultId}/restore")
    public ResponseEntity<VaultDTO> restore(@AuthenticationPrincipal User user, @PathVariable  UUID vaultId){
        Vault v = vaultService.restore(user, vaultId);
        return ResponseEntity.ok(VaultMapper.mapToDto(v));
    }

}
