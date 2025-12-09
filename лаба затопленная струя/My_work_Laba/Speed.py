import matplotlib.pyplot as plt
import numpy as np
import math

COEFFICIENT = 0.50012 
RHO = 1.3
ADC_atm = 212386.86

FILE_NAMES = [
    "d:\Filiki\My_work_Laba\mm0.txt",  # Файл 1
    "d:\Filiki\My_work_Laba\mm10.txt",  # Файл 2
    "d:\Filiki\My_work_Laba\mm20.txt",  # Файл 3
    "d:\Filiki\My_work_Laba\mm30.txt",  # Файл 4
    "d:\Filiki\My_work_Laba\mm40.txt",  # Файл 5
    "d:\Filiki\My_work_Laba\mm50.txt",  # Файл 6
    "d:\Filiki\My_work_Laba\mm60.txt",  # Файл 7
    "d:\Filiki\My_work_Laba\mm70.txt",  # Файл 8
    "d:\Filiki\My_work_Laba\mm80.txt",  # Файл 9
]

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
                        continue
            
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
    pressure_measurements = []
    
    for adc_value in adc_measurements:
        if adc_value - ADC_atm > 0:
            pressure_measurements.append((adc_value - ADC_atm) * COEFFICIENT)
        else:
            pressure_measurements.append(0)

    return pressure_measurements

def convert_to_velocity(pressure_measurements):
    """
    Преобразует давление в скорость струи воздуха по формуле: V = sqrt(2P/ρ)
    """
    
    velocity_measurements = []
    
    for P in pressure_measurements:
        pressure_diff = P - 117
        
        if pressure_diff > 0:
            velocity = math.sqrt(0.17 * pressure_diff / RHO)
            velocity_measurements.append(velocity)
        else:
            velocity_measurements.append(0)

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

def calculate_area_under_curve(x_values, y_values):
    """
    Вычисляет площадь под кривой методом трапеций
    """
    area = 0.0
    for i in range(1, len(x_values)):
        width = abs(x_values[i] - x_values[i-1])
        avg_height = (y_values[i] + y_values[i-1]) / 2.0
        area += width * avg_height
    
    return area

def plot_all_pressure(all_pressure_arrays, distances_arrays, file_names):
    """
    Строит график давления для всех файлов на одном графике
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Вычисляем площади под кривыми давления
    pressure_areas = []
    for i, (pressure_array, distances) in enumerate(zip(all_pressure_arrays, distances_arrays)):
        area = calculate_area_under_curve(distances, pressure_array)
        pressure_areas.append(area)
    
    # Рисуем графики для каждого файла
    for i, (pressure_array, distances, area) in enumerate(zip(all_pressure_arrays, distances_arrays, pressure_areas)):
        if i < len(COLORS):
            color = COLORS[i]
        else:
            color = 'black'  # если файлов больше чем цветов
        
        # Создаем метку с площадью
        short_name = file_names[i].split('\\')[-1]  # Изменено с '/' на '\\' для Windows путей
        label = f"Файл {i+1}: {short_name} (S={area:.2f})"
        
        ax.plot(distances, pressure_array, 
                color=color, linewidth=2, marker='o', markersize=3,
                label=label)
    
    # Настройки графика
    ax.set_xlabel('Координата трубки Пито, мм', fontsize=12)
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
    
    # Выводим информацию о площадях
    print("\nПлощади под графиками давления:")
    for i, area in enumerate(pressure_areas):
        short_name = file_names[i].split('\\')[-1]
        print(f"  Файл {i+1} ({short_name}): {area:.2f} Па·ед.")
    
    plt.show()
    
    return fig, ax, pressure_areas

def plot_all_velocity(all_velocity_arrays, distances_arrays, file_names):
    """
    Строит график скорости для всех файлов на одном графике
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Вычисляем площади под кривыми скорости
    velocity_areas = []
    for i, (velocity_array, distances) in enumerate(zip(all_velocity_arrays, distances_arrays)):
        area = calculate_area_under_curve(distances, velocity_array)
        velocity_areas.append(area)
    
    # Рисуем графики для каждого файла
    for i, (velocity_array, distances, area) in enumerate(zip(all_velocity_arrays, distances_arrays, velocity_areas)):
        if i < len(COLORS):
            color = COLORS[i]
        else:
            color = 'black'
        
        # Создаем метку с площадью
        short_name = file_names[i].split('\\')[-1]  # Изменено с '/' на '\\' для Windows путей
        label = f"Файл {i+1}: {short_name} ({area:.2f})"
        
        ax.plot(distances, velocity_array, 
                color=color, linewidth=2, marker='s', markersize=3,
                label=label)
    
    # Настройки графика
    ax.set_xlabel('Координата трубки Пито, мм', fontsize=12)
    ax.set_ylabel('Скорость, м/с', fontsize=12)
    ax.set_title('Зависимость скорости от расстояния (все измерения)', fontsize=14)
    ax.grid(True, alpha=0.3)
    
    # Легенда
    ax.legend(loc='best', fontsize=10)
    
    # Информация о формуле и площади
    ax.text(0.02, 0.98, f'Формула: V = √(2(P-P0)/ρ), ρ = {RHO} кг/м³', 
            transform=ax.transAxes, fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig("all_velocity_graphs.png", dpi=150)
    print("График скоростей для всех файлов сохранен как 'all_velocity_graphs.png'")
    
    # Выводим информацию о площадях
    print("\nПлощади под графиками скорости:")
    for i, area in enumerate(velocity_areas):
        short_name = file_names[i].split('\\')[-1]
        print(f"  Файл {i+1} ({short_name}): {area:.2f} (м/с)·ед.")
    
    plt.show()
    
    return fig, ax, velocity_areas

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
        
        # Вычисляем площадь под кривой
        area = calculate_area_under_curve(distances, pressure_array)
        
        # Получаем имя файла без пути
        short_name = file_names[i].split('\\')[-1]  # Изменено с '/' на '\\' для Windows путей
        
        ax.plot(distances, pressure_array, 'b-', linewidth=2, marker='o', markersize=3)
        ax.set_xlabel('Расстояние, усл. ед.', fontsize=10)
        ax.set_ylabel('Давление, Па', fontsize=10)
        ax.set_title(f'Файл {i+1}: {short_name}', fontsize=11)
        ax.grid(True, alpha=0.3)
        
        # Статистика на графике с площадью
        stats_text = f"Макс: {max(pressure_array):.1f} Па\nСр: {np.mean(pressure_array):.1f} Па\nПлощадь: {area:.2f} Па·ед."
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
        
        # Вычисляем площадь под кривой
        area = calculate_area_under_curve(distances, velocity_array)
        
        short_name = file_names[i].split('\\')[-1]  # Изменено с '/' на '\\' для Windows путей
        
        ax.plot(distances, velocity_array, 'r-', linewidth=2, marker='s', markersize=3)
        ax.set_xlabel('Расстояние, усл. ед.', fontsize=10)
        ax.set_ylabel('Скорость, м/с', fontsize=10)
        ax.set_title(f'Файл {i+1}: {short_name}', fontsize=11)
        ax.grid(True, alpha=0.3)
        
        stats_text = f"Макс: {max(velocity_array):.1f} м/с\nСр: {np.mean(velocity_array):.1f} м/с\nПлощадь: {area:.2f} (м/с)·ед."
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
            f.write(f"Формула скорости: V = √(2(P-P0)/ρ)\n")
            
            # Для каждого файла
            for file_idx, filename in enumerate(file_names):
                short_name = filename.split('\\')[-1]  # Изменено с '/' на '\\' для Windows путей
                f.write(f"\n{'='*60}\n")
                f.write(f"ФАЙЛ {file_idx+1}: {short_name}\n")
                f.write(f"{'='*60}\n\n")
                
                pressure_array = all_pressure_arrays[file_idx]
                velocity_array = all_velocity_arrays[file_idx]
                distances = distances_arrays[file_idx]
                
                f.write(f"Количество измерений: {len(pressure_array)}\n")
                
                # Вычисляем площади
                pressure_area = calculate_area_under_curve(distances, pressure_array)
                velocity_area = calculate_area_under_curve(distances, velocity_array)
                
                # Статистика давления
                f.write(f"\nДавление:\n")
                f.write(f"  Минимум: {min(pressure_array):.2f} Па\n")
                f.write(f"  Максимум: {max(pressure_array):.2f} Па\n")
                f.write(f"  Среднее: {np.mean(pressure_array):.2f} Па\n")
                f.write(f"  Медиана: {np.median(pressure_array):.2f} Па\n")
                f.write(f"  Площадь под кривой: {pressure_area:.2f} Па·ед.\n")
                
                # Статистика скорости
                f.write(f"\nСкорость:\n")
                f.write(f"  Минимум: {min(velocity_array):.2f} м/с\n")
                f.write(f"  Максимум: {max(velocity_array):.2f} м/с\n")
                f.write(f"  Среднее: {np.mean(velocity_array):.2f} м/с\n")
                f.write(f"  Медиана: {np.median(velocity_array):.2f} м/с\n")
                f.write(f"  Площадь под кривой: {velocity_area:.2f} (м/с)·ед.\n")
                
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
    _, _, pressure_areas = plot_all_pressure(all_pressure_arrays, distances_arrays, valid_files)
    
    # 5.2 Все измерения на одном графике (скорость)
    print("\n2. Все измерения скорости на одном графике:")
    _, _, velocity_areas = plot_all_velocity(all_velocity_arrays, distances_arrays, valid_files)
    
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
        short_name = valid_files[i].split('\\')[-1]
        
        # Вычисляем площади
        pressure_area = calculate_area_under_curve(distances_arrays[i], pressure)
        velocity_area = calculate_area_under_curve(distances_arrays[i], velocity)
        
        print(f"\nФайл {i+1} ({short_name}):")
        print(f"  Давление: {min(pressure):.1f} ... {max(pressure):.1f} Па (ср: {np.mean(pressure):.1f} Па)")
        print(f"  Площадь под кривой давления: {pressure_area:.2f} Па·ед.")
        print(f"  Скорость: {min(velocity):.1f} ... {max(velocity):.1f} м/с (ср: {np.mean(velocity):.1f} м/с)")
        print(f"  Площадь под кривой скорости: {velocity_area:.2f} (м/с)·ед.")

if __name__ == "__main__":
    main()
