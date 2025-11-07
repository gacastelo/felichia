from argon2.low_level import hash_secret_raw, Type

def derivar_chave(senha, salt):
    return hash_secret_raw(
        senha.encode(),
        salt,
        time_cost=3,
        memory_cost=64*1024,
        parallelism=2,
        hash_len=32,
        type=Type.ID
    )

