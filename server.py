import socket        # Comunicação em rede (UDP)
import json          # Serialização dos pacotes
import hashlib       # Cálculo do checksum
import time

# Endereço e porta do servidor
HOST = "127.0.0.1"
PORT = 5000

def verificar_checksum(pacote):
 return pacote["checksum"] == checksum(pacote["dados"])

print("=== SERVIDOR RDT 3.0 (Stop-and-Wait) ===")

# Criação do socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
sequencia_esperada = 0

while True:
    # Recebe pacote do cliente
    data, addr = sock.recvfrom(1024)
    pacote = json.loads(data.decode())

    print("\n[Servidor] Pacote recebido:")
    print(f"  Sequência: {pacote['seq']}")
    print(f"  Dados: {pacote['dados']}")
    print(f"  Checksum: {pacote['checksum']}")

    # Verifica se houve corrupção
    if not verificar_checksum(pacote):
        print("[Servidor] ❌ Pacote CORROMPIDO detectado.")
        print("[Servidor] Ignorando pacote (sem envio de ACK).")
        continue  # RDT 3.0 não usa NAK

    # Verifica se é um pacote duplicado
    if pacote["seq"] != sequencia_esperada:
        print("[Servidor] ⚠ Pacote duplicado detectado.")
        print("[Servidor] Reenviando ACK do último pacote válido.")

        ack = {"ack": 1 - sequencia_esperada}
        sock.sendto(json.dumps(ack).encode(), addr)
        continue

    # Pacote correto e esperado
    print("[Servidor] ✅ Pacote correto entregue à aplicação.")
    print(f"[Servidor] Dados entregues: {pacote['dados']}")

    # Envio do ACK correspondente
    ack = {"ack": sequencia_esperada}
    sock.sendto(json.dumps(ack).encode(), addr)
    print(f"[Servidor] ACK {sequencia_esperada} enviado.")
    sequencia_esperada = 1 - sequencia_esperada

