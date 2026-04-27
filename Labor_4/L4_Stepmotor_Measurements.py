"""-----------------------------------------------------
¦    File name: L4_Stepmotor_Measurements.py            s¦
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


# settings of stepper motor and cycles/movement
STEP_TIME = 0.002  # *** CHANGE ME *** time in [s] between two consecutive steps of stepper motor
MOVEMENT_STOP_TIME = 0  # *** CHANGE ME ***  Pause [s] between two consecutive movements (up/down) of slide on linear guideway
MOVEMENT_STEP_NUMBER = 2000  # *** CHANGE ME ***  Number of steps to drive the stepper motor per movement of the slide on the linear guideway
CYCLE_START_DIRECTION = 1  # *** CHANGE ME ***  Direction (0 or 1) of first movement of slide on linear guideway
CYCLE_NUMBER = 3  # *** CHANGE ME ***  Number of cycles (movement of slide on linear guideway in one direction, followed by movement in the opposite direction)


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
    lgpio.gpio_write(gpio0, IN1,  coil_1)
    lgpio.gpio_write(gpio0, IN2,  coil_2)
    lgpio.gpio_write(gpio0, IN3,  coil_3)
    lgpio.gpio_write(gpio0, IN4,  coil_4)


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
        time.sleep(secs - secs / 10)
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

    # initialize all pins to safe stat
    lgpio.gpio_write(gpio0, IN1, 0)
    lgpio.gpio_write(gpio0, IN2, 0)
    lgpio.gpio_write(gpio0, IN3, 0)
    lgpio.gpio_write(gpio0, IN4, 0)


    """ start measurement """
    try:
        direction = CYCLE_START_DIRECTION
        step = 0
        cycle = 0
        # endless loop
        while cycle < CYCLE_NUMBER:
            if direction == 0:
                while step < MOVEMENT_STEP_NUMBER:
                    # activate coil 2 & coil 4
                    set_motor_coils(0, 1, 0, 1)
                    busy_sleep(STEP_TIME)
                    
                    step += 1

                    if step >= MOVEMENT_STEP_NUMBER:
                        break  # leave while-loop
                    # activate coil 2 & coil 3
                    set_motor_coils(0, 1, 1, 0)
                    busy_sleep(STEP_TIME)
                    step += 1

                    if step >= MOVEMENT_STEP_NUMBER:
                        break  # leave while-loop
                    # activate coil 1 & coil 3
                    set_motor_coils(1, 0, 1, 0)
                    busy_sleep(STEP_TIME)
                    step += 1

                    if step >= MOVEMENT_STEP_NUMBER:
                        break  # leave while-loop
                    # activate coil 1 & coil 4
                    set_motor_coils(1, 0, 0, 1)
                    busy_sleep(STEP_TIME)
                    step += 1

                    if step >= MOVEMENT_STEP_NUMBER:
                        break  # leave while-loop
            elif direction == 1:
                while step < MOVEMENT_STEP_NUMBER:
                    # activate coil 1 & coil 4
                    set_motor_coils(1, 0, 0, 1)
                    busy_sleep(STEP_TIME)
                    step += 1

                    if step >= MOVEMENT_STEP_NUMBER:
                        break  # leave while-loop
                    # activate coil 1 & coil 3
                    set_motor_coils(1, 0, 1, 0)
                    busy_sleep(STEP_TIME)
                    step += 1

                    if step >= MOVEMENT_STEP_NUMBER:
                        break  # leave while-loop
                    # activate coil 2 & coil 3
                    set_motor_coils(0, 1, 1, 0)
                    busy_sleep(STEP_TIME)
                    step += 1

                    if step >= MOVEMENT_STEP_NUMBER:
                        break  # leave while-loop
                    # activate coil 2 & coil 4
                    set_motor_coils(0, 1, 0, 1)
                    busy_sleep(STEP_TIME)
                    step += 1

            step = 0
            direction = not direction  # change direction
            cycle += 0.5

            # check if last movement of measurement is not already done
            if cycle != CYCLE_NUMBER:
                # wait between movements
                time.sleep(MOVEMENT_STOP_TIME)

        stop_motor()
        # Free GPIO pins
        lgpio.gpio_free(gpio0, IN1)
        lgpio.gpio_free(gpio0, IN2)
        lgpio.gpio_free(gpio0, IN3)
        lgpio.gpio_free(gpio0, IN4) # Close the GPIO chip connection
        print("Exit Python")
        exit(0)  # exit python with exit code 0

    # detect exception - usually triggered by a user input, stopping the script
    except KeyboardInterrupt:
        stop_motor()
        # Free GPIO pins
        lgpio.gpio_free(gpio0, IN1)
        lgpio.gpio_free(gpio0, IN2)
        lgpio.gpio_free(gpio0, IN3)
        lgpio.gpio_free(gpio0, IN4)  # Close the GPIO chip connection
        print("Exit Python")
        exit(0)  # exit python with exit code 0