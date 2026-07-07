package dev.gacastelo.felichia.config;

import org.springframework.context.annotation.Configuration;

@Configuration
public class Config {
    public final static int daysToDeleteDisabledUsers = 3;
    public final static int daysToDeleteDisabledVaults = 4;
    public final static String JWT_SECRET = System.getenv("JWT_SECRET");
}
