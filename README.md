# 🎮 GameBots: Środowisko w Pygame do trenowania i porównywania agentów uczenia nadzorowanego oraz Reinforcement Learning (PPO)
Checkout my report about this project on my Website: https://bit.ly/game_bots

A BBTAN clone built in Python (Pygame) as an AI sandbox. This project explores and compares different Artificial Intelligence approaches: from pure math (Aimbot) and Machine Learning (Random Forest), up to advanced Reinforcement Learning (PPO).

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)
![Stable Baselines3](https://img.shields.io/badge/Stable_Baselines3-PPO-orange.svg)
![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-Machine_Learning-yellow.svg)

Witaj w projekcie **GameBots**! Celem tego repozytorium jest stworzenie od podstaw klona popularnej gry mobilnej **BBTAN** (w bibliotece Pygame), a następnie zbadanie i porównanie różnych podejść do sztucznej inteligencji, która uczy się w nią grać. 

Od losowych strzałów, przez twardą matematykę, aż po zaawansowane sieci neuronowe – ten projekt to kompletne laboratorium testowe dla algorytmów AI.

---

## 🧠 Nasi Agenci (Podejścia do AI)

W ramach projektu zaimplementowano i przetestowano cztery różne typy "mózgów" sterujących grą:

### 1. 🎲 Random Bot (Baseline)
Najprostszy możliwy agent. Wybiera całkowicie losowy kąt strzału. Służy jako punkt odniesienia (baseline) do oceny, czy bardziej zaawansowane modele w ogóle się czegoś uczą. Średnio przegrywa w okolicach 10. poziomu.

### 2. 🎯 Math Aimbot (Nauczyciel)
Algorytm oparty na czystej matematyce i geometrii. Oblicza idealne trajektorie i rykoszety. Gra bezbłędnie i służy jako "nauczyciel" do generowania idealnych danych treningowych (setki tysięcy wierszy z informacjami o stanie planszy i idealnym kącie strzału).

### 3. 📚 Supervised Learning Agent (Uczeń)
Model uczenia nadzorowanego (np. `RandomForestRegressor` / `RandomForestClassifier`), trenowany na ogromnej bazie danych wygenerowanej przez Aimbota.
* **Wyniki:** Bot szybko łapie podstawy i potrafi regularnie dochodzić do ~24 poziomu.
* **Wnioski:** Ujawnia klasyczny "szklany sufit" algorytmów regresyjnych. W gęstych, krytycznych sytuacjach model uśrednia decyzje (zamiast wybrać ryzykowny rykoszet), co prowadzi do nieuniknionej przegranej w okolicach 30. poziomu.

### 4. 🏋️ Reinforcement Learning Agent (PPO - Mistrz)
Prawdziwa sztuczna inteligencja oparta na uczeniu ze wzmocnieniem (Reinforcement Learning), wykorzystująca algorytm **PPO (Proximal Policy Optimization)** z biblioteki `stable-baselines3`.
* Model nie korzysta z gotowych wzorów matematycznych – uczy się fizyki gry samodzielnie metodą prób i błędów, maksymalizując nagrody za zbijanie klocków i przetrwanie.
* **Wyniki:** Po odpowiednio długim treningu (ponad 65k+ kroków) agent potrafi przetrwać ponad **600 poziomów**, skutecznie utrzymując klocki z dala od dolnej krawędzi ekranu (średnio na 9. piętrze z 10 możliwych).

---

## 📊 Analiza Danych i Trening

Projekt kładzie duży nacisk na analitykę i śledzenie postępów AI. W folderach projektu znajdują się skrypty do analizy danych przy użyciu biblioteki `pandas`.

* **Eksploracja TensorBoard:** Uczenie agenta PPO jest na bieżąco monitorowane, co pozwala zaobserwować klasyczne krzywe uczenia (np. wczesny spadek formy podczas eksploracji i późniejszy, stabilny wzrost średniej nagrody oraz długości życia bota).
* **Histogramy Skuteczności:** Wizualizacja "szklanego sufitu" bota SL, udowadniająca ograniczenia uczenia nadzorowanego w środowiskach wymagających precyzyjnych decyzji na ułamki stopni.

*(Tutaj możesz w przyszłości dodać swoje zrzuty ekranu z wykresami, używając tagu `![Opis](sciezka/do/obrazka.png)`)*

---

## 🛠 Technologie i Wymagania

* **Python** 3.8+
* **Pygame:** Silnik fizyki i renderowania gry.
* **Pandas / NumPy / Matplotlib:** Zbieranie danych, macierze stanu i generowanie wykresów.
* **Scikit-learn:** Uczenie nadzorowane (Machine Learning).
* **Stable-Baselines3:** Algorytmy uczenia ze wzmocnieniem (PPO).

---

## 🚀 Jak zagrać i uruchomić projekt

Skopiuj repozytorium na swój dysk:
```bash
git clone [https://github.com/Borsh8m3/Gamebots.git](https://github.com/Borsh8m3/Gamebots.git)
cd Gamebots

Zainstaluj wymagane biblioteki:
pip install -r requirements.txt

Głównym plikiem jest notatnik Main.ipynb

Tryb Manualny (Zagraj sam!)
Możesz samodzielnie przetestować fizykę gry. Wystarczy uruchomić główny plik gry, nacisnąć lewy przycisk myszy, naciągnąć i wycelować:
python game.py
