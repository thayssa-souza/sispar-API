from flask_bcrypt import bcrypt

def hash_senha(senha):
    salt = bcrypt.gensalt() # Gera um salt/hash aleatório para a senha em bytes
    return bcrypt.hashpw(senha.encode('utf-8'), salt) # Retorna a senha criptografada em bytes, com o salt gerado acima
    # passamos o ecode para avisar que a senha está vindo em utf-8 e vamos transformar em bytes
    

def checar_senha(senha, senha_hash):
    # Verifica se a senha informada é igual a senha armazenada no banco de dados
    return bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8')) 
    # O checkpw vai comparar a senha que foi passada com o hash que está armazenado no banco de dados, e retorna True ou False
    
    
    