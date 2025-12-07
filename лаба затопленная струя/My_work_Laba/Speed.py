import matplotlib.pyplot as plt
import numpy as np
import math

# Коэффициент преобразования (отсчеты АЦП в паскали)
COEFFICIENT = 37.375  # отсчет/Паскаль
# Плотность воздуха (кг/м^3)
RHO = 1.3

# Список файлов с измерениями
# ФАЙЛ 1: mm0.txt - базовая настройка
# ФАЙЛ 2: mm1.txt - первое измерение
# ФАЙЛ 3: mm2.txt - второе измерение
# ФАЙЛ 4: mm3.txt - третье измерение
# ФАЙЛ 5: mm4.txt - четвертое измерение
# ФАЙЛ 6: mm5.txt - пятое измерение
# ФАЙЛ 7: mm6.txt - шестое измерение
# ФАЙЛ 8: mm7.txt - седьмое измерение
# ФАЙЛ 9: mm8.txt - восьмое измерение

FILE_NAMES = [
    "D:/forpython/My_GitHub/get/лаба затопленная струя/My_work_Laba/mm0.txt",  # Файл 1
    "D:/forpython/My_GitHub/get/лаба затопленная струя/My_work_Laba/mm1.txt",  # Файл 2
    "D:/forpython/My_GitHub/get/лаба затопленная струя/My_work_Laba/mm2.txt",  # Файл 3
    "D:/forpython/My_GitHub/get/лаба затопленная струя/My_work_Laba/mm3.txt",  # Файл 4
    "D:/forpython/My_GitHub/get/лаба затопленная струя/My_work_Laba/mm4.txt",  # Файл 5
    "D:/forpython/My_GitHub/get/лаба затопленная струя/My_work_Laba/mm5.txt",  # Файл 6
    "D:/forpython/My_GitHub/get/лаба затопленная струя/My_work_Laba/mm6.txt",  # Файл 7
    "D:/forpython/My_GitHub/get/лаба затопленная струя/My_work_Laba/mm7.txt",  # Файл 8
    "D:/forpython/My_GitHub/get/лаба затопленная струя/My_work_Laba/mm8.txt",  # Файл 9
]

# Цвета для разных файлов
COLORS = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive']

def read_adc_measurements(filename):
    """
    Читает один файл с измерениями АЦП
    """
    try:
        with open(filename, 'r') as file:
            measurements = []
            for line in file:
                line = line.strip()
                if line:
                    try:
                        adc_value = float(line)
                        measurements.append(adc_value)
                    except ValueError:
                        continue  # просто пропускаем нечисла
            
            if not measurements:
                print(f"Файл '{filename}' пуст")
                return None
            
            print(f"Прочитано {len(measurements)} измерений из {filename}")
            return measurements
            
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла '{filename}': {e}")
        return None

def read_all_adc_measurements(file_names):
    """
    Читает все файлы с измерениями АЦП
    Возвращает список массивов измерений
    """
    all_measurements = []
    valid_files = []
    
    for i, filename in enumerate(file_names):
        print(f"\nЧтение файла {i+1}: {filename}")
        measurements = read_adc_measurements(filename)
        if measurements is not None:
            all_measurements.append(measurements)
            valid_files.append(filename)
            print(f"  Успешно: {len(measurements)} измерений")
        else:
            print(f"  Пропущен")
    
    return all_measurements, valid_files

def convert_to_pressure(adc_measurements):
    """
    Преобразует отсчеты АЦП в давление в паскалях
    """
    pressure_measurements = [adc_value / COEFFICIENT for adc_value in adc_measurements]
    return pressure_measurements

def convert_to_velocity(pressure_measurements):
    """
    Преобразует давление в скорость струи воздуха по формуле: V = sqrt(2P/ρ)
    """
    velocity_measurements = [math.sqrt(2 * P / RHO) for P in pressure_measurements]
    return velocity_measurements

def create_distances_array(measurement_count):
    """
    Создает массив расстояний для заданного количества измерений
    """
    distances = []
    p = 0.054945  # шаг расстояния
    k = -2.8      # начальное расстояние
    
    for i in range(measurement_count):
        distances.append(k)
        k += p
    
    return distances

def plot_all_pressure(all_pressure_arrays, distances_arrays, file_names):
    """
    Строит график давления для всех файлов на одном графике
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Рисуем графики для каждого файла
    for i, (pressure_array, distances) in enumerate(zip(all_pressure_arrays, distances_arrays)):
        if i < len(COLORS):
            color = COLORS[i]
        else:
            color = 'black'  # если файлов больше чем цветов
        
        # Создаем метку из имени файла
        label = f"Файл {i+1}: {file_names[i].split('/')[-1]}"
        
        ax.plot(distances, pressure_array, 
                color=color, linewidth=2, marker='o', markersize=3,
                label=label)
    
    # Настройки графика
    ax.set_xlabel('Расстояние, усл. ед.', fontsize=12)
    ax.set_ylabel('Давление, Па', fontsize=12)
    ax.set_title('Зависимость давления от расстояния (все измерения)', fontsize=14)
    ax.grid(True, alpha=0.3)
    
    # Легенда
    ax.legend(loc='best', fontsize=10)
    
    # Информация о коэффициенте
    ax.text(0.02, 0.98, f'Коэффициент: {COEFFICIENT} отсчет/Паскаль', 
            transform=ax.transAxes, fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig("all_pressure_graphs.png", dpi=150)
    print("\nГрафик давлений для всех файлов сохранен как 'all_pressure_graphs.png'")
    plt.show()
    
    return fig, ax

def plot_all_velocity(all_velocity_arrays, distances_arrays, file_names):
    """
    Строит график скорости для всех файлов на одном графике
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Рисуем графики для каждого файла
    for i, (velocity_array, distances) in enumerate(zip(all_velocity_arrays, distances_arrays)):
        if i < len(COLORS):
            color = COLORS[i]
        else:
            color = 'black'
        
        label = f"Файл {i+1}: {file_names[i].split('/')[-1]}"
        
        ax.plot(distances, velocity_array, 
                color=color, linewidth=2, marker='s', markersize=3,
                label=label)
    
    # Настройки графика
    ax.set_xlabel('Расстояние, усл. ед.', fontsize=12)
    ax.set_ylabel('Скорость, м/с', fontsize=12)
    ax.set_title('Зависимость скорости от расстояния (все измерения)', fontsize=14)
    ax.grid(True, alpha=0.3)
    
    # Легенда
    ax.legend(loc='best', fontsize=10)
    
    # Информация о формуле
    ax.text(0.02, 0.98, f'Формула: V = √(2P/ρ), ρ = {RHO} кг/м³', 
            transform=ax.transAxes, fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig("all_velocity_graphs.png", dpi=150)
    print("График скоростей для всех файлов сохранен как 'all_velocity_graphs.png'")
    plt.show()
    
    return fig, ax

def plot_pressure_for_each_file(all_pressure_arrays, distances_arrays, file_names):
    """
    Строит отдельные графики давления для каждого файла
    """
    n_files = len(all_pressure_arrays)
    n_cols = 3  # 3 графика в строке
    n_rows = (n_files + n_cols - 1) // n_cols  # округление вверх
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 4*n_rows))
    axes = axes.flatten() if n_files > 1 else [axes]
    
    for i, (pressure_array, distances) in enumerate(zip(all_pressure_arrays, distances_arrays)):
        ax = axes[i]
        
        # Получаем имя файла без пути
        short_name = file_names[i].split('/')[-1]
        
        ax.plot(distances, pressure_array, 'b-', linewidth=2, marker='o', markersize=3)
        ax.set_xlabel('Расстояние, усл. ед.', fontsize=10)
        ax.set_ylabel('Давление, Па', fontsize=10)
        ax.set_title(f'Файл {i+1}: {short_name}', fontsize=11)
        ax.grid(True, alpha=0.3)
        
        # Статистика на графике
        stats_text = f"Макс: {max(pressure_array):.1f} Па\nСр: {np.mean(pressure_array):.1f} Па"
        ax.text(0.98, 0.98, stats_text, transform=ax.transAxes, fontsize=9,
                verticalalignment='top', horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Скрываем пустые графики
    for i in range(n_files, len(axes)):
        axes[i].set_visible(False)
    
    plt.tight_layout()
    plt.savefig("individual_pressure_graphs.png", dpi=150)
    print("Индивидуальные графики давлений сохранены как 'individual_pressure_graphs.png'")
    plt.show()

def plot_velocity_for_each_file(all_velocity_arrays, distances_arrays, file_names):
    """
    Строит отдельные графики скорости для каждого файла
    """
    n_files = len(all_velocity_arrays)
    n_cols = 3
    n_rows = (n_files + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 4*n_rows))
    axes = axes.flatten() if n_files > 1 else [axes]
    
    for i, (velocity_array, distances) in enumerate(zip(all_velocity_arrays, distances_arrays)):
        ax = axes[i]
        
        short_name = file_names[i].split('/')[-1]
        
        ax.plot(distances, velocity_array, 'r-', linewidth=2, marker='s', markersize=3)
        ax.set_xlabel('Расстояние, усл. ед.', fontsize=10)
        ax.set_ylabel('Скорость, м/с', fontsize=10)
        ax.set_title(f'Файл {i+1}: {short_name}', fontsize=11)
        ax.grid(True, alpha=0.3)
        
        stats_text = f"Макс: {max(velocity_array):.1f} м/с\nСр: {np.mean(velocity_array):.1f} м/с"
        ax.text(0.98, 0.98, stats_text, transform=ax.transAxes, fontsize=9,
                verticalalignment='top', horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    for i in range(n_files, len(axes)):
        axes[i].set_visible(False)
    
    plt.tight_layout()
    plt.savefig("individual_velocity_graphs.png", dpi=150)
    print("Индивидуальные графики скоростей сохранены как 'individual_velocity_graphs.png'")
    plt.show()

def save_all_results(all_pressure_arrays, all_velocity_arrays, distances_arrays, file_names):
    """
    Сохраняет все результаты в один файл
    """
    try:
        with open("все_результаты_расчетов.txt", 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("РЕЗУЛЬТАТЫ РАСЧЕТОВ ДЛЯ ВСЕХ ФАЙЛОВ\n")
            f.write("="*80 + "\n\n")
            
            f.write(f"Коэффициент АЦП: {COEFFICIENT} отсчет/Паскаль\n")
            f.write(f"Плотность воздуха: {RHO} кг/м³\n")
            f.write(f"Формула скорости: V = √(2P/ρ)\n\n")
            
            # Для каждого файла
            for file_idx, filename in enumerate(file_names):
                short_name = filename.split('/')[-1]
                f.write(f"\n{'='*60}\n")
                f.write(f"ФАЙЛ {file_idx+1}: {short_name}\n")
                f.write(f"{'='*60}\n\n")
                
                pressure_array = all_pressure_arrays[file_idx]
                velocity_array = all_velocity_arrays[file_idx]
                distances = distances_arrays[file_idx]
                
                f.write(f"Количество измерений: {len(pressure_array)}\n")
                
                # Статистика давления
                f.write(f"\nДавление:\n")
                f.write(f"  Минимум: {min(pressure_array):.2f} Па\n")
                f.write(f"  Максимум: {max(pressure_array):.2f} Па\n")
                f.write(f"  Среднее: {np.mean(pressure_array):.2f} Па\n")
                f.write(f"  Медиана: {np.median(pressure_array):.2f} Па\n")
                
                # Статистика скорости
                f.write(f"\nСкорость:\n")
                f.write(f"  Минимум: {min(velocity_array):.2f} м/с\n")
                f.write(f"  Максимум: {max(velocity_array):.2f} м/с\n")
                f.write(f"  Среднее: {np.mean(velocity_array):.2f} м/с\n")
                f.write(f"  Медиана: {np.median(velocity_array):.2f} м/с\n")
                
                # Первые 10 значений
                f.write(f"\nПервые 10 значений:\n")
                f.write(f"№\tРасстояние\tДавление (Па)\tСкорость (м/с)\n")
                f.write(f"{'-'*50}\n")
                
                for i in range(min(10, len(pressure_array))):
                    f.write(f"{i+1}\t{distances[i]:.4f}\t\t"
                           f"{pressure_array[i]:.2f}\t\t{velocity_array[i]:.2f}\n")
                
                if len(pressure_array) > 10:
                    f.write(f"... и еще {len(pressure_array) - 10} значений\n")
        
        print("\nВсе результаты сохранены в файл 'все_результаты_расчетов.txt'")
        
    except Exception as e:
        print(f"Ошибка при сохранении результатов: {e}")

def main():
    print("="*60)
    print("ОБРАБОТКА 9 ФАЙЛОВ С ИЗМЕРЕНИЯМИ АЦП")
    print("="*60)
    
    # 1. Чтение всех файлов
    print("\n=== ЧТЕНИЕ ФАЙЛОВ ===")
    all_adc_measurements, valid_files = read_all_adc_measurements(FILE_NAMES)
    
    if not all_adc_measurements:
        print("Нет данных для обработки")
        return
    
    print(f"\nУспешно прочитано {len(all_adc_measurements)} файлов из {len(FILE_NAMES)}")
    
    # 2. Преобразование в давление
    print("\n=== ПРЕОБРАЗОВАНИЕ В ДАВЛЕНИЕ ===")
    all_pressure_arrays = []
    for i, adc_measurements in enumerate(all_adc_measurements):
        pressure = convert_to_pressure(adc_measurements)
        all_pressure_arrays.append(pressure)
        print(f"Файл {i+1}: {len(pressure)} значений давления")
    
    # 3. Преобразование в скорость
    print("\n=== ПРЕОБРАЗОВАНИЕ В СКОРОСТЬ ===")
    all_velocity_arrays = []
    for i, pressure_array in enumerate(all_pressure_arrays):
        velocity = convert_to_velocity(pressure_array)
        all_velocity_arrays.append(velocity)
        print(f"Файл {i+1}: макс. скорость = {max(velocity):.1f} м/с")
    
    # 4. Создание массивов расстояний для каждого файла
    print("\n=== СОЗДАНИЕ МАССИВОВ РАССТОЯНИЙ ===")
    distances_arrays = []
    for pressure_array in all_pressure_arrays:
        distances = create_distances_array(len(pressure_array))
        distances_arrays.append(distances)
        print(f"Диапазон: {distances[0]:.3f} ... {distances[-1]:.3f}")
    
    # 5. Построение графиков
    print("\n=== ПОСТРОЕНИЕ ГРАФИКОВ ===")
    
    # 5.1 Все измерения на одном графике (давление)
    print("\n1. Все измерения давления на одном графике:")
    plot_all_pressure(all_pressure_arrays, distances_arrays, valid_files)
    
    # 5.2 Все измерения на одном графике (скорость)
    print("\n2. Все измерения скорости на одном графике:")
    plot_all_velocity(all_velocity_arrays, distances_arrays, valid_files)
    
    # 5.3 Отдельные графики для каждого файла (давление)
    print("\n3. Отдельные графики давления для каждого файла:")
    plot_pressure_for_each_file(all_pressure_arrays, distances_arrays, valid_files)
    
    # 5.4 Отдельные графики для каждого файла (скорость)
    print("\n4. Отдельные графики скорости для каждого файла:")
    plot_velocity_for_each_file(all_velocity_arrays, distances_arrays, valid_files)
    
    # 6. Сохранение результатов
    print("\n=== СОХРАНЕНИЕ РЕЗУЛЬТАТОВ ===")
    save_all_results(all_pressure_arrays, all_velocity_arrays, distances_arrays, valid_files)
    
    # 7. Итоговая статистика
    print("\n=== ИТОГОВАЯ СТАТИСТИКА ===")
    print(f"\nОбработано файлов: {len(all_pressure_arrays)}")
    
    for i in range(len(all_pressure_arrays)):
        pressure = all_pressure_arrays[i]
        velocity = all_velocity_arrays[i]
        short_name = valid_files[i].split('/')[-1]
        
        print(f"\nФайл {i+1} ({short_name}):")
        print(f"  Давление: {min(pressure):.1f} ... {max(pressure):.1f} Па (ср: {np.mean(pressure):.1f} Па)")
        print(f"  Скорость: {min(velocity):.1f} ... {max(velocity):.1f} м/с (ср: {np.mean(velocity):.1f} м/с)")

if __name__ == "__main__":
    main()
