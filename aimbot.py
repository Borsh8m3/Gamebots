import math
import time
from game import BBTAN, Block

def get_best_angle(real_game):
    best_angle = -math.pi / 2  # Domyślnie prosto w górę
    max_damage_score = -1

    print("Symulowanie trajektorii...")
    
    # Testujemy kąty od 15 do 165 stopni (skok co 5 stopni)
    # Im mniejszy skok (np. co 1 stopień), tym bot celniejszy, ale myśli dłużej!
    for deg in range(15, 166, 5):
        test_angle_rad = -math.pi * deg / 180.0
        
        # 1. Tworzymy "klona" gry (render_mode=False, żeby działało błyskawicznie w tle)
        sim = BBTAN(render_mode=False)
        
        # 2. Kopiujemy idealnie stan z prawdziwej gry do symulacji
        sim.level = real_game.level
        sim.max_balls = real_game.max_balls
        sim.start_x = real_game.start_x
        sim.start_y = real_game.start_y
        sim.done = real_game.done
        
        sim.blocks = []
        for b in real_game.blocks:
            # Tworzymy nowe obiekty klocków, żeby nie zepsuć prawdziwej planszy
            new_b = Block(b.col, b.row, b.hp)
            new_b.rect.x = b.rect.x
            new_b.rect.y = b.rect.y
            sim.blocks.append(new_b)
            
        # 3. Odpalamy symulację JEDNEJ tury dla tego kąta
        # step() z game.py zwraca nagrodę (reward), która jest wyższa, im więcej HP zbijemy
        _, reward, _, _ = sim.step(test_angle_rad)
        
        # 4. Sprawdzamy, czy ten strzał był najlepszy
        if reward > max_damage_score:
            max_damage_score = reward
            best_angle = test_angle_rad
            
    return best_angle, max_damage_score

# ==========================================
# GŁÓWNA PĘTLA GRY
# ==========================================
if __name__ == "__main__":
    # Uruchamiamy prawdziwą grę (widoczną na ekranie)
    env = BBTAN(render_mode=True)
    
    while not env.done:
        # Obliczamy najlepszy ruch
        start_time = time.time()
        best_angle, expected_score = get_best_angle(env)
        calc_time = time.time() - start_time
        
        angle_deg = abs(math.degrees(best_angle))
        print(f"Najlepszy kąt: {angle_deg:.1f}° | Spodziewany wynik: {expected_score:.1f} | Czas myślenia: {calc_time:.2f}s")
        
        # Wykonujemy prawdziwy strzał!
        env.step(best_angle)
        
    print(f"Koniec gry! Agent dotarł do poziomu {env.level}")