"""-----------------------------------------------------
¦    File name: L4_DCmotor.py                           ¦
¦    Version: 1.1                                       ¦
¦    Authors:                                           ¦
¦       Jonas Josi                                      ¦
¦       Matthias Lang                                   ¦
¦       Christian Hohmann                               ¦
¦       Joschka Maters                                  ¦
¦    Date created: 2024/05/01                           ¦
¦    Last modified: 2026/01/20                          ¦
¦    Python Version: 3.11.2                             ¦
------------------------------------------------------"""

# ----------- import external Python module -----------
import lgpio  # library to create hardware-based PWM signals on Raspberry Pi


# ----------- global constant -----------
# assign L298N motor driver interface to GPIO's of Raspberry Pi
IN1 = 17    # IN1 on Motor screw terminal
IN2 = 18    # IN2 on Motor screw terminal 
ENA = 12    # ENA - PWM for speed control (Enable A)

# settings
VOLTAGE = 6 # *** CHANGE ME *** voltage for DC motor [V] between 0 und 12 V (Voltage from power supply is always 12 V)
DIRECTION = 1  # *** CHANGE ME *** movement direction (0 or 1) of slide on linear guideway

# auxiliary parameters
MAX_VOLTAGE = 12  # supply voltage of motor driver is 12 V (which equals the max. rated voltage of the DC motor)
PWM_FREQUENCY = 1000  # Hz
PWM_DUTYCYCLE = round(VOLTAGE / MAX_VOLTAGE * 100, 3)  # PWM_DUTYCYCLE from 0 (OFF) to 100 percent (FULLY ON)


# ----------- function definition -----------
def stop_motor():
    """
    Stop the motor by setting both IN1 and IN2 to LOW,
    and setting PWM duty cycle to 0%.
    """
    # set state of motor driver outputs (M1 and M2) to low (0 V)
    lgpio.gpio_write(gpio0, IN1, 0)
    lgpio.gpio_write(gpio0, IN2, 0)

    # disable motor by setting PWM duty cycle to 0%
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

    print(f"Motor settings:")
    print(f"  Voltage: {VOLTAGE}V (max: {MAX_VOLTAGE}V)")
    print(f"  Direction: {DIRECTION}")
    print(f"  PWM Frequency: {PWM_FREQUENCY}Hz")
    print(f"  PWM Duty Cycle: {PWM_DUTYCYCLE}%")

    """ run motor """
    try:
        if DIRECTION == 0:
            # set direction: IN1 HIGH, IN2 LOW
            lgpio.gpio_write(gpio0, IN1, 1)
            lgpio.gpio_write(gpio0, IN2, 0)
            # set PWM signal on D1 (enable pin) for speed contro
            lgpio.tx_pwm(gpio0, ENA, PWM_FREQUENCY, PWM_DUTYCYCLE)

        elif DIRECTION == 1:
            # set direction: IN1 LOW, IN2 HIGH  
            lgpio.gpio_write(gpio0, IN1, 0)
            lgpio.gpio_write(gpio0, IN2, 1)
            # set PWM signal on ENA
            lgpio.tx_pwm(gpio0, ENA, PWM_FREQUENCY, PWM_DUTYCYCLE)            
  
        # Ask for any user input to stop motor / script
        userinput = input("Stop motor? (Press Enter for yes)")
        stop_motor()
        # Free GPIO pins
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