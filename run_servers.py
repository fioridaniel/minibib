#!/usr/bin/env python3
"""
Script de teste para o sistema Minibib.com
Testa todas as operações básicas do sistema.
"""

import subprocess
import time
import sys
import threading
import os

def run_server(script_path, args, name):
    """Executa um servidor em uma thread separada"""
    cmd = [sys.executable, script_path] + args
    print(f"[{name}] Iniciando com comando: {' '.join(cmd)}")
    try:
        subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"[{name}] Iniciado")
    except Exception as e:
        print(f"[{name}] Erro: {e}")

def main():
    print("="*60)
    print("TESTE DO SISTEMA MINIBIB.COM")
    print("="*60)
    
    # Mudar para o diretório do projeto
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    print("\n1 - Iniciando Servidor de Catálogo (porta 50051)...")
    threading.Thread(
        target=run_server,
        args=("backend/catalogue_server.py", ["50051"], "Catálogo"),
        daemon=True
    ).start()
    time.sleep(2)
    
    print("\n2 - Iniciando Servidor de Pedidos (porta 50052)...")
    threading.Thread(
        target=run_server,
        args=("backend/orders_server.py", ["50052", "localhost:50051"], "Pedidos"),
        daemon=True
    ).start()
    time.sleep(2)
    
    print("\n3 - Iniciando Servidor Front-end (porta 50050)...")
    threading.Thread(
        target=run_server,
        args=("frontend/frontend-server.py", ["50050", "localhost:50051", "localhost:50052"], "Frontend"),
        daemon=True
    ).start()
    time.sleep(2)
    
    print("\n" + "="*60)
    print("TODOS OS SERVIDORES INICIADOS")
    print("="*60)
    print("\n4 - Para testar o cliente, execute em outro terminal:")
    print(f"   cd {project_dir}")
    print("   python client/client.py localhost:50050")
    print("\nPressione CTRL+C para parar os servidores\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nEncerrando servidores...")
        sys.exit(0)

if __name__ == "__main__":
    main()
