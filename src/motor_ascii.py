import time
import os

class InterpreteASCII:
    def __init__(self):
        self.texturas = {
            "Pasto": "🌱",
            "Agua": "🌊",
            "Lava": "🔥",
            "Paloma": "🕊️",
            "Aguila": "🦅",
            "Nave": "🚀"
        }
        self.dino = "🦖"

    def animar(self, mapa_plano):
        input("\n🎮 ¡Compilación exitosa! Presione ENTER para iniciar la simulación...")
        
        for i in range(len(mapa_plano)):
            # Limpieza nativa y segura para la terminal de VS Code / PowerShell
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("=" * 50)
            print("           🦖 SIMULADOR DINO ENGINE 🦖")
            print("=" * 50 + "\n")
            
            # --- 1. DIBUJAMOS EL MAPA ---
            capa_mapa = ""
            for bloque in mapa_plano:
                textura = self.texturas.get(bloque, "?")
                capa_mapa += textura + " " # El emoji + el espacio ocupan aprox 3 columnas
                
            # --- 2. DIBUJAMOS AL DINO ---
            # Multiplicamos "3 espacios" por la posición actual para empujarlo exacto
            espacios_izq = "   " * i
            capa_dino = espacios_izq + self.dino
            
            # Imprimimos al Dino y luego el piso
            print(capa_dino)
            print(capa_mapa)
            
            print(f"\n📍 Posición actual: {mapa_plano[i]}")
            print(f"📊 Progreso del nivel: {i + 1}/{len(mapa_plano)}")
            
            # Subimos el tiempo a 0.4 para que se mueva a un ritmo visible y disfrutable
            time.sleep(0.4) 
            
        print("\n✨ ¡MISIÓN CUMPLIDA! El dinosaurio escapó con éxito. ✨\n")