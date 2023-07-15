
#Source https://www.raspberrypi-spy.co.uk/2012/07/16x2-lcd-module-control-using-python/

#import
import RPi.GPIO as GPIO
import time

# Define GPIO to LCD mapping
LCD_RS = 1 #RS (Register Select) = 4 on LCD
LCD_E = 26 #Enable or Strobe = 6 on LCD
LCD_D4 = 12 #Data Bit 4 = 11 on LCD
LCD_D5 = 16 #Data Bit 5 = 12 on LCD
LCD_D6 = 20 #Data Bit 6 = 13 on LCD
LCD_D7 = 21 #Data Bit 7 = 14 on LCD

# Define device constants
LCD_WIDTH = 16
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0

#Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#GPIO.OUT list
GPIO_OUT_LIST = [LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7]
DATA_BITS = {LCD_D4:[0x10,0x01], LCD_D5:[0x20,0x02], LCD_D6:[0x40,0x04], LCD_D7:[0x80,0x08]}

def main():
    GPIO.setwrarnings(False)
    GPIO.setmode(GPIO.BCM)
    for out_pin in GPIO_OUT_LIST:
        GPIO.setup(out_pin, GPIO.OUT)

    # Initialise display
    lcd_init()


def lcd_init():
    # Initialise display
    lcd_byte(0x33,LCD_CMD)
    lcd_byte(0x32,LCD_CMD)
    lcd_byte(0x06,LCD_CMD)
    lcd_byte(0x0C,LCD_CMD)
    lcd_byte(0x28,LCD_CMD)
    lcd_byte(0x01,LCD_CMD)
    time.sleep(E_DELAY)

def lcd_byte(bits, mode):
    GPIO.output(LCD_RS, mode)

    for pos in [0,1]: # High bits = 0, Low bits = 1
        for data_pin in DATA_BITS:
            GPIO.output(data_pin, False)
        
        for data_pin, data_bits in DATA_BITS.items():
            if bits&data_bits[pos]==data_bits[pos]:
                GPIO.output(data_pin, True)
        
        # Toggle 'Enable' pin
        lcd_toggle_enable()

def lcd_toggle_enable():
    # Toggle enable
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)

def lcd_string(message, line=LCD_LINE_1):
    # Send string to display
    message = message.ljust(LCD_WIDTH, " ")

    lcd_byte(line, LCD_CMD)

    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)


main()

lcd_string("Working!")
lcd_string("Both lines", LCD_LINE_2)
time.sleep(3)

#To display
lcd_byte(0x01, LCD_CMD)
lcd_string("Goodbye!", LCD_LINE_1)
GPIO.cleanup()