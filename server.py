import socket
from utils import parse_packet, is_corrupted

HOST = "127.0.0.1"
PORT = 12000

print("=== SERVIDOR RDT 3.0 (Stop-and-Wait) ===")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

sequencia_esperada = 0

while True:
    data, addr = sock.recvfrom(1024)

    packet = data.decode()
    seq, dados, chksum = parse_packet(packet)

    print("\n[Servidor] Pacote recebido:")
    print(f"  Sequência: {seq}")
    print(f"  Dados: {dados}")

    if is_corrupted(dados, chksum):
        print("[Servidor] ❌ Pacote corrompido. Ignorado.")
        continue  # RDT 3.0 não envia NAK

    if seq != sequencia_esperada:
        print("[Servidor] ⚠ Pacote duplicado.")
        ack = f"ACK{1 - sequencia_esperada}"
        sock.sendto(ack.encode(), addr)
        continue

    print("[Servidor] ✅ Pacote entregue à aplicação.")

    ack = f"ACK{sequencia_esperada}"
    sock.sendto(ack.encode(), addr)
    print(f"[Servidor] ACK {sequencia_esperada} enviado.")

    sequencia_esperada = 1 - sequencia_esperada

