# libraries
import RPi.GPIO as GPIO
import time
import sqlite3

GPIO.setmode(GPIO.BCM)

GPIO_TRIG = 23
GPIO_ECHO = 24

GPIO.setup (GPIO_TRIG, GPIO.OUT)
GPIO.setup (GPIO_ECHO, GPIO.IN)
GPIO.output(GPIO_TRIG, False)

def get_distance():
	GPIO.output(GPIO_TRIG, True)
	time.sleep(0.00001)  # 10 microseconds
	GPIO.output(GPIO_TRIG, False)

	while GPIO.input(GPIO_ECHO) == 0:
		StartTime = time.time()

	while GPIO.input(GPIO_ECHO) == 1:
		StopTime = time.time()

	TimeElapsed = StopTime - StartTime

	distance = TimeElapsed*17150
	distance = round(distance,2)

	return distance

def log_data(dist):
	conn = sqlite3.connect('sensorsdata.db')
	curs = conn.cursor()

	curs.execute("INSERT INTO HCSR04_data values(datetime('now', 'localtime'),(?))",(dist, ))
	conn.commit()
	conn.close()

def display_data():
	conn = sqlite3.connect('sensorsdata.db')
	curs = conn.cursor()
	print("\nEntire database contents:\n")
	for row in curs.execute("SELECT * FROM HCSR04_data"):
		print(row)
	conn.close()

if __name__ == '__main__':
	try:
		while True:
			dist = get_distance() 
			log_data(dist)
			print("Distance is %.2f cm" % dist)
			time.sleep(2)

	except KeyboardInterrupt:
		display_data()
		print("Measurment stopped by user\n")
		GPIO.cleanup()
