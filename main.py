from nvidia_racecar import NvidiaRacecar
import time

def main():
    print("Hello World!")
    car = NvidiaRacecar()
    print("Set up!")
    
    car.steering = 1
    time.sleep(1)
    print(car.throttle_gain)
    car.throttle = 0.15
    
    
    start_time = time.time()
    
    while (car.steering > 0.0 and time.time() - start_time < 20):
        car.steering -= 0.005
        time.sleep(0.5)
    
    print("Done")
    car.throttle = 0.0
    
    print("Goodbye World... :(")
    
    
    
if __name__ == '__main__':
    main()