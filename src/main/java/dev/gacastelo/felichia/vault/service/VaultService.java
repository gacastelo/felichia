package dev.gacastelo.felichia.vault.service;

import dev.gacastelo.felichia.auth.userCustomer.UserCustomDetails;
import dev.gacastelo.felichia.config.Config;
import dev.gacastelo.felichia.exceptions.NaoEncontradoException;
import dev.gacastelo.felichia.exceptions.VersaoDesatualizadaException;
import dev.gacastelo.felichia.user.entity.User;
import dev.gacastelo.felichia.user.repository.UserRepository;
import dev.gacastelo.felichia.vault.VaultMapper;
import dev.gacastelo.felichia.vault.dto.VaultCreateRequest;
import dev.gacastelo.felichia.vault.dto.VaultDTO;
import dev.gacastelo.felichia.vault.dto.VaultUpdateRequest;
import dev.gacastelo.felichia.vault.entity.Vault;
import dev.gacastelo.felichia.vault.repository.VaultRepository;
import jakarta.transaction.Transactional;
import jakarta.validation.Valid;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.RequestBody;

import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.UUID;


@Service
public class VaultService {

    private final VaultRepository vaultRepository;
    private final UserRepository userRepository;

    public VaultService(VaultRepository vaultRepository, UserRepository userRepository) {
        this.vaultRepository = vaultRepository;
        this.userRepository = userRepository;
    }

    @Transactional
    public Vault create(UserCustomDetails user, VaultCreateRequest request) {
        if (vaultRepository.existsByUserIdAndDeletedAtIsNull(user.getId())) {
            throw new IllegalStateException("O usuário já possui um Vault ativoUserCustomDetails");
        }
        User userEntity = userRepository.findById(user.getId()).orElseThrow(() -> new NaoEncontradoException("Usúario Não encontrado" + user.getId()));
        return vaultRepository.save(new Vault(userEntity, request));
    }

    public VaultDTO getMyVault(UserCustomDetails user) {
        Vault vault = vaultRepository.findByUserIdAndDeletedAtIsNull(user.getId()).orElseThrow(() -> new NaoEncontradoException("Não foram encontrados Vaults habilitados para o usuário de id: " + user.getId()));
        return VaultMapper.mapToDto(vault);
    }

    @Transactional
    public VaultDTO update(UserCustomDetails user, VaultUpdateRequest request) {
        Vault vault = vaultRepository.findByUserIdAndDeletedAtIsNull(user.getId()).orElseThrow(() -> new NaoEncontradoException("Não foram encontrados Vaults habilitados para o usuário de id: " + user.getId()));

        if (!request.version().equals(vault.getVersion() + 1)) {
            throw new VersaoDesatualizadaException("Esperava versão " + (vault.getVersion() + 1) + ", mas recebeu " + request.version());
        }

        vault.update(request.vaultData(), request.version());

        return VaultMapper.mapToDto(vault);
    }

    @Transactional
    public void disable(UserCustomDetails user) {
        Vault v = vaultRepository.findByUserIdAndDeletedAtIsNull(user.getId()).orElseThrow(() -> new NaoEncontradoException("Não foram encontrados Vaults habilitados para o usuário de id: " + user.getId()));
        v.setDeletedAt(Instant.now());
    }

    @Transactional
    public Vault restore(UserCustomDetails user, UUID vaultId) {
        Vault vault = vaultRepository.findById(vaultId).orElseThrow(() -> new NaoEncontradoException("Vault não encontrado: " + vaultId));

        if (!vault.getUser().getId().equals(user.getId())) {
            throw new AccessDeniedException("Vault não pertence ao usuário.");
        }

        if (vault.getDeletedAt() == null) {
            throw new IllegalStateException("O Vault já está ativo.");
        }

        if (vaultRepository.existsByUserIdAndDeletedAtIsNull(user.getId())){
            throw new IllegalStateException("Não é possível restaurar um vault com outro já ativo.");
        }
        vault.setDeletedAt(null);
        return vault;
    }

    @Scheduled(cron = "0 0 0 * * *")
    @Transactional
    public void deleteDisabledVaults() {
        Instant limite = Instant.now().minus(Config.daysToDeleteDisabledVaults, ChronoUnit.DAYS);

        List<Vault> disabledVaults = vaultRepository.findAllByDeletedAtIsBefore(limite);

        vaultRepository.deleteAll(disabledVaults);
    }
}
