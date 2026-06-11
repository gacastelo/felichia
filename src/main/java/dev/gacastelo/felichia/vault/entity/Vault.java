package dev.gacastelo.felichia.vault.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import dev.gacastelo.felichia.user.entity.User;
import jakarta.persistence.*;
import jakarta.validation.constraints.Positive;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(
        name = "vaults",
        indexes = {
                @Index(name = "idx_vault_user_id", columnList = "user_id")
        }
)
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Vault {

    @Id
    @Column(unique = true, nullable = false)
    private UUID id;

    @OneToOne
    @JoinColumn(name = "user_id", unique = true, nullable = false)
    @JsonIgnore
    private User user;

    @Lob
    @Column(name = "vault_data", nullable = false)
    private byte[] vaultData;

    @Column(nullable = false)
    private byte[] salt;

    @Column(nullable = false)
    private byte[] nonce;

    @Column(nullable = false)
    private boolean enabled;

    @Column(nullable = false)
    @Positive
    private Integer version;

    @Column(name = "created_at", nullable = false)
    private Instant createdAt;

    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    @PrePersist
    public void prePersist() {
        if (id == null) id = UUID.randomUUID();
        if (createdAt == null) createdAt = Instant.now();
        if (updatedAt == null) updatedAt = Instant.now();
    }

    @PreUpdate
    public void preUpdate() {
        updatedAt = Instant.now();

    }

    public Vault(User user) {
        this.user = user;
        this.salt = user.getSalt();
    }
}
