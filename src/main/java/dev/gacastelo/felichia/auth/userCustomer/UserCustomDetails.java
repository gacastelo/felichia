package dev.gacastelo.felichia.auth.userCustomer;

import dev.gacastelo.felichia.user.entity.User;
import lombok.Getter;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.util.Collection;
import java.util.UUID;

@Getter
public class UserCustomDetails implements UserDetails {
    private final UUID id;
    private final String username;
    private final String email;
    private final boolean emailVerified;
    private final String password;
    private final Collection<? extends GrantedAuthority>  authorities;


    public UserCustomDetails(User user) {
        this.id = user.getId();
        this.username = user.getUsername();
        this.email = user.getEmail();
        this.emailVerified = user.isEmailVerified();
        this.password = user.getPassword();
        this.authorities = user.getAuthorities();
    }
}
