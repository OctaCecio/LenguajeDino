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
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("=" * 50)
            print("           🦖 EJECUCIÓN DINO 🦖")
            print("=" * 50 + "\n")
            
            capa_mapa = ""
            for bloque in mapa_plano:
                textura = self.texturas.get(bloque, "?")
                capa_mapa += textura + " " 
                
           
            espacios_izq = "   " * i
            capa_dino = espacios_izq + self.dino
        
            print(capa_dino)
            print(capa_mapa)
            
            print(f"\n Posición actual: {mapa_plano[i]}")
            print(f" Progreso del nivel: {i + 1}/{len(mapa_plano)}")
            
            
            time.sleep(0.4) 
            
        print("\n ¡MISIÓN CUMPLIDA! El dinosaurio escapó con éxito.\n")