"""-----------------------------------------------------
¦    File name: Motor_off.py                            ¦
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

## Import Packages
import lgpio


class Motor_Off:
    """ Class to correctly turn of the DC motor oder Stepper motor """
    def turn_motor_off():
        """ Definition to turn of the motor driver channels and drivers """

        # Set ports and settings
        IN1 = 17 	# A  or M1
        IN2 = 18  	# A/ or M2
        IN3 = 27     # B  or M3
        IN4 = 22     # B/ or M4
        ENA = 12     # N  -> Turn on the motordriver A A/

        # Turn on Motordrivers -> 1
        lgpio(gpio0, ENA, 1)


        # Set channels to 0
        lgpio(gpio0, IN1, 0)
        lgpio(gpio0, IN2, 0)
        lgpio(gpio0, IN3, 0)
        lgpio(gpio0, IN4, 0)

        # Turn off Motordrivers -> 0
        lgpio(gpio0, ENA, 0)

        print("Motor turned off")


# When this program is run
if __name__ == '__main__':
    # run defined method to turn of the motor
    gpio0 = lgpio.gpiochip_open(0)  # Open GPIO chip 0
    Motor_Off.turn_motor_off()