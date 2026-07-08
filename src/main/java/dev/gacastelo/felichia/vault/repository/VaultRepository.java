package dev.gacastelo.felichia.vault.repository;

import dev.gacastelo.felichia.vault.entity.Vault;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;

import java.time.Instant;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

public interface VaultRepository extends JpaRepository<Vault, UUID>, JpaSpecificationExecutor<Vault> {
    boolean existsByUserIdAndDeletedAtIsNull(UUID userId);
    Optional<Vault> findByUserIdAndDeletedAtIsNull(UUID userId);

    List<Vault> findAllByDeletedAtIsBefore(Instant now);
}
