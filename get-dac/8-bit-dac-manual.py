import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)


dinamic_range = 3.17
dac_bits = [16, 20, 32, 35, 26, 17, 27, 22]
GPIO.setup(dac_bits, GPIO.OUT)

def voltage_to_number(voltage):
    if not(0.0 <= voltage <= dinamic_range):
        print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {dinamic_range:.2f} B")
        print("Устанавливаем 0.0 В")
        return 0

    return int(voltage / dinamic_range * 255)

def number_to_dac(number):
    bits = [int(element) for element in bin(number)[2:].zfill(8)]
    print(f"Число на вход ЦАП: {number}, биты: {bits}")
    GPIO.output(dac_bits, bits)

try:
    while True:
        try:
            voltage = float(input("Введите напряжение в Вольтах: "))
            number = voltage_to_number(voltage)
            number_to_dac(number)

        except ValueError:
            print("Вы ввели не число. Попробуйте ещё раз\n")

finally:
    GPIO.output(dac_bits, 0)
    GPIO.cleanup()
