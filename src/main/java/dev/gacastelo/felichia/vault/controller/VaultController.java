package dev.gacastelo.felichia.vault.controller;


import dev.gacastelo.felichia.auth.userCustomer.UserCustomDetails;
import dev.gacastelo.felichia.user.entity.User;
import dev.gacastelo.felichia.user.service.UserService;
import dev.gacastelo.felichia.vault.VaultMapper;
import dev.gacastelo.felichia.vault.dto.VaultCreateRequest;
import dev.gacastelo.felichia.vault.dto.VaultDTO;
import dev.gacastelo.felichia.vault.dto.VaultUpdateRequest;
import dev.gacastelo.felichia.vault.entity.Vault;
import dev.gacastelo.felichia.vault.service.VaultService;
import jakarta.validation.Valid;
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
    public ResponseEntity<VaultDTO> getVault(@AuthenticationPrincipal UserCustomDetails user) {
        return ResponseEntity.ok(vaultService.getMyVault(user));
    }

    @PostMapping
    public ResponseEntity<VaultDTO> createVault(@AuthenticationPrincipal UserCustomDetails user, @Valid @RequestBody VaultCreateRequest request){
        Vault v = vaultService.create(user, request);
        return ResponseEntity.ok(VaultMapper.mapToDto(v));
    }

    @PutMapping
    public ResponseEntity<VaultDTO> updateVault(@AuthenticationPrincipal UserCustomDetails user, @Valid @RequestBody VaultUpdateRequest request) {
        return ResponseEntity.ok(vaultService.update(user, request));
    }

    @DeleteMapping
    public ResponseEntity<Void> deleteVault(@AuthenticationPrincipal UserCustomDetails user) {
        vaultService.disable(user);
        return ResponseEntity.ok().build();
    }

    @PostMapping("{vaultId}/restore")
    public ResponseEntity<VaultDTO> restore(@AuthenticationPrincipal UserCustomDetails user, @PathVariable  UUID vaultId){
        Vault v = vaultService.restore(user, vaultId);
        return ResponseEntity.ok(VaultMapper.mapToDto(v));
    }

}
