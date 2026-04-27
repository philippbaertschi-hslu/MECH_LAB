"""-----------------------------------------------------
¦    File name: L4_DCmotor_Measurements.py              ¦
¦    Version: 1.1                                       ¦
¦    Authors:                                           ¦
¦       Jonas Josi                                      ¦
¦       Matthias Lang                                   ¦
¦       Christian Hohmann                               ¦
¦       Joschka Maters                                  ¦
¦    Date created: 2024/05/01                           ¦
¦    Last modified: 2025/01/20                          ¦
¦    Python Version: 3.11.2                             ¦
------------------------------------------------------"""

# ----------- import external Python module -----------
import lgpio  # library to create hardware-based PWM signals on Raspberry Pi
import time

# ----------- global constant -----------
# assign motor driver interface to GPIO's of Raspberry Pi
IN1 = 17    # IN1 on Motor screw terminal 
IN2 = 18    # IN2 on Motor screw terminal
ENA = 12    # ENA - PWM for speed control (Enable A)

# settings
VOLTAGE = 12  # *** CHANGE ME *** Voltage for DC motor [V] between 0 und 12 V (Voltage from power supply is always 12 V)
MOVEMENT_DRIVE_TIME = 1  # *** CHANGE ME *** Time in [s] to drive the DC motor for each movement
MOVEMENT_STOP_TIME = 2  # *** CHANGE ME ***  Pause in [s] between two consecutive movements (up/down) of slide on linear guideway
CYCLE_START_DIRECTION = 1  # *** CHANGE ME ***  Direction (0 or 1) of first movement of slide on linear guideway
CYCLE_NUMBER = 3  # *** CHANGE ME ***  Number of cycles (movement of slide on linear guideway in one direction, followed by movement in the opposite direction)

# auxiliary parameters
MAX_VOLTAGE = 12  # supply voltage of motor driver is 12 V (which equals the max. rated voltage of the DC motor)
PWM_FREQUENCY = 1000  # Hz
PWM_DUTYCYCLE = round(VOLTAGE / MAX_VOLTAGE * 100, 3)  # PWM_DUTYCYCLE from 0 (OFF) to 100 % (FULLY ON)


# ----------- function definition -----------
def stop_motor():
    """
    Stop the motor by setting both IN1 and IN2 to LOW,
    and setting PWM duty cycle to 0%.
    """
    # set state of motor driver outputs (IN1 and IN2) to low (0 V)
    lgpio.gpio_write(gpio0, IN1, 0)
    lgpio.gpio_write(gpio0, IN2, 0)

    # disable motor driver by setting PWM duty cycle to 0%
    lgpio.tx_pwm(gpio0, ENA, PWM_FREQUENCY, 0)

    print("\nMotor stopped")


# ----------- main code -----------
if __name__ == "__main__":
    # initialize lgpio
    gpio0 = lgpio.gpiochip_open(0)  # Open GPIO chip 0

    # Configure GPIO pins as outputs
    lgpio.gpio_claim_output(gpio0, IN1)
    lgpio.gpio_claim_output(gpio0, IN2) 
    lgpio.gpio_claim_output(gpio0, ENA)
    
    # Initialize all pins to safe state
    lgpio.gpio_write(gpio0, IN1, 0)
    lgpio.gpio_write(gpio0, IN2, 0)
    lgpio.tx_pwm(gpio0, ENA, PWM_FREQUENCY, 0)  # PWM at 0% initially

    """ start measurement """
    try:
        direction = CYCLE_START_DIRECTION
        cycle = 0
        # endless loop
        while cycle < CYCLE_NUMBER:
            if direction == 0:
                # set direction: IN1 HIGH, IN2 LOW
                lgpio.gpio_write(gpio0, IN1, 1)
                lgpio.gpio_write(gpio0, IN2, 0)
                # set PWM signal 
                lgpio.tx_pwm(gpio0, ENA, PWM_FREQUENCY, PWM_DUTYCYCLE)
                time.sleep(MOVEMENT_DRIVE_TIME)
                # stop motor
                lgpio.tx_pwm(gpio0, ENA, PWM_FREQUENCY, 0)
            elif direction == 1:
                # set direction: IN1 HIGH, IN2 LOW
                lgpio.gpio_write(gpio0, IN1, 0)
                lgpio.gpio_write(gpio0, IN2, 1)
                # set PWM signal 
                lgpio.tx_pwm(gpio0, ENA, PWM_FREQUENCY, PWM_DUTYCYCLE)
                time.sleep(MOVEMENT_DRIVE_TIME)
                # stop motor
                lgpio.tx_pwm(gpio0, ENA, PWM_FREQUENCY, 0)

            direction = not direction  # change direction
            cycle += 0.5

            # check if last movement of measurement is not already done
            if cycle != CYCLE_NUMBER:
                # wait between movements
                time.sleep(MOVEMENT_STOP_TIME)

        stop_motor()
        #Free GPIO pins
        lgpio.gpio_free(gpio0, IN1)
        lgpio.gpio_free(gpio0, IN2)
        lgpio.gpio_free(gpio0, ENA)
        lgpio.gpiochip_close(gpio0)  # Close the GPIO chip connection
        print("Exit Python")
        exit(0)  # exit python with exit code 0

    # detect exception - usually triggered by a user input, stopping the script
    except KeyboardInterrupt:
        stop_motor()
        # Free GPIO pins
        lgpio.gpio_free(gpio0, IN1)
        lgpio.gpio_free(gpio0, IN2)
        lgpio.gpio_free(gpio0, ENA)
        lgpio.gpiochip_close(gpio0)  # Close the GPIO chip connection
        print("Exit Python")
        exit(0)  # exit python with exit code 0