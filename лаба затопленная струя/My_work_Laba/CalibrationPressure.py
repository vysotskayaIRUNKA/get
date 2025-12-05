import matplotlib.pyplot as plt
import numpy as np

P_max = 108000  # 108 кПа = 108000 Па
P_atm = 0       # Атмосферное за 0 Па

ADC_atm = 212386.86
ADC_max = 215276.47826086957

#расчет коэффициента
KOEFFICIENT = round((P_max - P_atm) / (ADC_max - ADC_atm), 3)
print(f"Коэффициент K = {KOEFFICIENT:.6f} Па/отсчёт")
print(f"Это значит: {1/KOEFFICIENT:.4f} отсчётов на 1 Па")

y1_correct = P_atm + KOEFFICIENT * (ADC_atm - ADC_atm)  # = 0 Па
y2_correct = P_atm + KOEFFICIENT * (ADC_max - ADC_atm)  # = 108000 Па

print(f"\nПравильные значения:")
print(f"При ADC={ADC_atm:.2f} -> P={y1_correct:.2f} Па (должно быть 0)")
print(f"При ADC={ADC_max:.2f} -> P={y2_correct:.2f} Па (должно быть {P_max})")

ADC_min_plot = ADC_atm
ADC_max_plot = ADC_max
ADC_range = np.linspace(ADC_min_plot, ADC_max_plot, 100)

P_range_correct = P_atm + KOEFFICIENT * (ADC_range - ADC_atm)

# Построение графиков
plt.figure(figsize=(12, 6))

# Основной график с правильной калибровкой
plt.plot(ADC_range, P_range_correct, 'b-', linewidth=2, label='Калибровочная прямая')

# Оси и сетка
plt.xlabel('Отсчеты АЦП', fontsize=12)
plt.ylabel('Давление, Па', fontsize=12)
plt.title('Правильная калибровка\nP = K × (ADC - ADC_atm)', fontsize=14)
plt.grid(True, alpha=0.3)

# Подписи точек
plt.annotate(f'Атмосферное\nADC={ADC_atm:.1f}\nP=0 Па', 
             xy=(ADC_atm, y1_correct), xytext=(ADC_atm-800, 30000),
             arrowprops=dict(arrowstyle='->', color='red'),
             fontsize=10, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))

plt.annotate(f'{P_max/1000:.0f} кПа\nADC={ADC_max:.1f}\nP={P_max} Па', 
             xy=(ADC_max, y2_correct), xytext=(ADC_max-600, 80000),
             arrowprops=dict(arrowstyle='->', color='red'),
             fontsize=10, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))

plt.legend()
plt.tight_layout()

# Калибровочные точки
plt.plot([ADC_atm, ADC_max], [y1_correct, y2_correct], 'bo', markersize=8, label='Калибровочные точки')

plt.xlabel('Отсчеты АЦП', fontsize=12)
plt.ylabel('Давление, Па', fontsize=12)
plt.title('Калибровка давления АЦП', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()

# Формулы на графике
plt.text(0.05, 0.95, f'K = {KOEFFICIENT:.6f} Па/отсчёт', 
         transform=plt.gca().transAxes, fontsize=11,
         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

plt.tight_layout()
plt.show()

# Дополнительная информация
print(f"\n=== ИТОГ ===")
print(f"Формула для преобразования АЦП в давление:")
print(f"P = {KOEFFICIENT:.6f} × (ADC - {ADC_atm:.2f})")