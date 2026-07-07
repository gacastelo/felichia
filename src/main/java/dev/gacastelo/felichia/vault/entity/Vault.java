package dev.gacastelo.felichia.vault.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import dev.gacastelo.felichia.user.entity.User;
import jakarta.persistence.*;
import jakarta.validation.constraints.Positive;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;

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
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "user_id", nullable = false)
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
    @Positive
    private Integer version;

    @Column(name = "created_at", nullable = false)
    private Instant createdAt;

    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    @Column(name = "deleted_at")
    private Instant deletedAt = null;

    @PrePersist
    public void prePersist() {
        if (id == null) id = UUID.randomUUID();
        if (createdAt == null) createdAt = Instant.now();
        if (updatedAt == null) updatedAt = Instant.now();
        if (version == null) version = 1;
    }

    @PreUpdate
    public void preUpdate() {
        updatedAt = Instant.now();
        version += 1;
    }

    public Vault(User user) {
        this.user = user;
    }

    public void update(byte[] vaultData, byte[] salt, byte[] nonce, Integer version) {
        this.vaultData = vaultData;
        this.salt = salt;
        this.nonce = nonce;
        this.version = version;
    }
}
