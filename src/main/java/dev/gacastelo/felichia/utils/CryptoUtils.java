package dev.gacastelo.felichia.utils;

import java.security.SecureRandom;

public final class CryptoUtils {

    private static final SecureRandom RANDOM = new SecureRandom();

    private CryptoUtils() {}

    public static byte[] randomBytes(int length) {
        byte[] bytes = new byte[length];
        RANDOM.nextBytes(bytes);
        return bytes;
    }
}
