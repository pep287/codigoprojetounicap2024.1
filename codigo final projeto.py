import RPi.GPIO as GPIO
import time

TRIG_PIN = 23  
ECHO_PIN = 24  
GREEN_LED_PIN = 17  
YELLOW_LED_PIN = 27  
RED_LED_PIN = 18  


GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
GPIO.setup(YELLOW_LED_PIN, GPIO.OUT)
GPIO.setup(RED_LED_PIN, GPIO.OUT)

def measure_distance():
    try:
        
        GPIO.output(TRIG_PIN, GPIO.HIGH)
        time.sleep(0.00001) 
        GPIO.output(TRIG_PIN, GPIO.LOW)
        
        
        pulse_start = time.time()
        while GPIO.input(ECHO_PIN) == 0:
            pulse_start = time.time()
        
       
        pulse_end = time.time()
        while GPIO.input(ECHO_PIN) == 1:
            pulse_end = time.time()
        
        
        pulse_duration = pulse_end - pulse_start
        
        
        distance = pulse_duration * 17150  
        distance = round(distance, 2)  
        
        return distance
    except Exception as e:
        print(f"Erro ao medir distância: {e}")
        return None

def set_leds(distance):
    
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)
    GPIO.output(YELLOW_LED_PIN, GPIO.LOW)
    GPIO.output(RED_LED_PIN, GPIO.LOW)
    
    
    if distance is None:
        return  
    elif distance > 100:
        GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
    elif 30 < distance <= 100:
        GPIO.output(YELLOW_LED_PIN, GPIO.HIGH)
    elif distance <= 30:
        GPIO.output(RED_LED_PIN, GPIO.HIGH)

try:
    print("Iniciando a medição de distância (Ctrl+C para sair)")
    time.sleep(2) 

    while True:
        dist = measure_distance()
        if dist is not None and dist <= 500:
            print(f"Distância: {dist} cm")
        set_leds(dist)
        time.sleep(0.1)  

except KeyboardInterrupt:
    print("Programa interrompido pelo usuário")

finally:
    GPIO.cleanup()  


def test_measure_distance():
    distance = measure_distance()
    assert distance is None or (distance >= 0 and distance <= 500), "A medição da distância deve estar dentro do intervalo esperado."

def test_set_leds():
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)
    GPIO.output(YELLOW_LED_PIN, GPIO.LOW)
    GPIO.output(RED_LED_PIN, GPIO.LOW)
    
    set_leds(150)
    assert GPIO.input(GREEN_LED_PIN) == GPIO.HIGH and GPIO.input(YELLOW_LED_PIN) == GPIO.LOW and GPIO.input(RED_LED_PIN) == GPIO.LOW, "LED verde deve estar aceso para distância > 100 cm."
    
    set_leds(50)
    assert GPIO.input(GREEN_LED_PIN) == GPIO.LOW and GPIO.input(YELLOW_LED_PIN) == GPIO.HIGH and GPIO.input(RED_LED_PIN) == GPIO.LOW, "LED amarelo deve estar aceso para distância entre 20 cm e 100 cm."
    
    set_leds(10)
    assert GPIO.input(GREEN_LED_PIN) == GPIO.LOW and GPIO.input(YELLOW_LED_PIN) == GPIO.LOW and GPIO.input(RED_LED_PIN) == GPIO.HIGH, "LED vermelho deve estar aceso para distância < 20 cm."

    set_leds(None)
    assert GPIO.input(GREEN_LED_PIN) == GPIO.LOW and GPIO.input(YELLOW_LED_PIN) == GPIO.LOW and GPIO.input(RED_LED_PIN) == GPIO.LOW, "Todos os LEDs devem estar apagados se a distância for None."


test_measure_distance()
test_set_leds()
