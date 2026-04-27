"""-----------------------------------------------------
¦    File name: L4_Stepmotor.py                         ¦
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
import lgpio
import time


# ----------- global constant -----------
# assign motor driver interface to GPIO's of Raspberry Pi
IN1 = 17    # Coil A+
IN2 = 18    # Coil A-
IN3 = 27    # Coil B+
IN4 = 22    # Coil B-

# settings of stepper motor
DIRECTION = 0  # *** CHANGE ME *** movement direction (0 or 1) of slide on linear guideway
STEP_TIME = 0.002  # *** CHANGE ME *** time in [s] between two consecutive steps of stepper motor

# ----------- function definition -----------
def set_motor_coils(coil_1, coil_2, coil_3, coil_4):
    """
    Set state (HIGH/LOW) of all 4 coils of stepper motor by controlling the output pins of the motor driver (IN1, IN2, IN3, IN4).
    Parameters
    ----------
    coil_1 : int or GPIO.LOW or GPIO.HIGH
    coil_2 : int or GPIO.LOW or GPIO.HIGH
    coil_3 : int or GPIO.LOW or GPIO.HIGH
    coil_4 : int or GPIO.LOW or GPIO.HIGH
    """
    lgpio.gpio_write(gpio0, IN1, coil_1)
    lgpio.gpio_write(gpio0, IN2, coil_2)
    lgpio.gpio_write(gpio0, IN3, coil_3)
    lgpio.gpio_write(gpio0, IN4, coil_4)


def busy_sleep(secs):
    """
    Actively waits for a specified time by keeping the CPU busy in a loop. This has the advantage over a passive sleep
    (i.e. time.sleep()) that a more precise timing / sleep time can be achieved. However, it may consume more
    CPU resources compared to a passive sleep method.

    Parameters
    ----------
    secs : float
        The wait time in seconds. Can be a decimal number.
    """
    start_timestamp = time.time()
    # if sleep time is more than 4 ms, make a passive sleep of sleep time - 2 ms to reduce cpu resources
    if secs > 0.0004:
        time.sleep(secs - 0.0002)
    while time.time() - start_timestamp < secs:
        pass  # do nothing


def stop_motor():
    """
    Set state of all 4 coils of stepper motor to LOW by controlling the output pins of the motor driver (IN1, IN2, IN3, IN4).
    Then disable all motor driver output pins (IN1, IN2, IN3, IN4).
    """

    # turn off all coils
    set_motor_coils(0, 0, 0, 0)
    busy_sleep(STEP_TIME)

    print("\nMotor stopped")


# ----------- main code -----------
if __name__ == "__main__":
    # initialize lgpio
    gpio0 = lgpio.gpiochip_open(0) # open GPIO chip 0

    # Configure GPIO pins as outputs
    lgpio.gpio_claim_output(gpio0, IN1)
    lgpio.gpio_claim_output(gpio0, IN2)
    lgpio.gpio_claim_output(gpio0, IN3)
    lgpio.gpio_claim_output(gpio0, IN4)

    # initialize all pins to safe state 
    lgpio.gpio_write(gpio0, IN1, 0)
    lgpio.gpio_write(gpio0, IN2, 0)
    lgpio.gpio_write(gpio0, IN3, 0)
    lgpio.gpio_write(gpio0, IN4, 0)


    try:
        # endless loop
        while True:
            if DIRECTION == 0:
                # activate coil 2 & coil 4
                set_motor_coils(0, 1, 0, 1)
                busy_sleep(STEP_TIME)
                # activate coil 2 & coil 3
                set_motor_coils(0, 1, 1, 0)
                busy_sleep(STEP_TIME)
                # activate coil 1 & coil 3
                set_motor_coils(1, 0, 1, 0)
                busy_sleep(STEP_TIME)
                # activate coil 1 & coil 4
                set_motor_coils(1, 0, 0, 1)
                busy_sleep(STEP_TIME)
            else:
                # activate coil 1 & coil 4
                set_motor_coils(1, 0, 0, 1)
                busy_sleep(STEP_TIME)
                # activate coil 1 & coil 3
                set_motor_coils(1, 0, 1, 0)
                busy_sleep(STEP_TIME)
                # activate coil 2 & coil 3
                set_motor_coils(0, 1, 1, 0)
                busy_sleep(STEP_TIME)
                # activate coil 2 & coil 4
                set_motor_coils(0, 1, 0, 1)
                busy_sleep(STEP_TIME)

    # detect exception - usually triggered by a user input, stopping the script
    except KeyboardInterrupt:
        stop_motor()
        # Free GPIO pins
        lgpio.gpio_free(gpio0, IN1)
        lgpio.gpio_free(gpio0, IN2)
        lgpio.gpio_free(gpio0, IN3)
        lgpio.gpio_free(gpio0, IN4)
        lgpio.gpiochip_close(gpio0) # Close the GPIO chip connection
        print("Exit Python")
        exit(0)  # exit python with exit code 0