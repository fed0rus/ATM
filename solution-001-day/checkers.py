from output_util import print_error


def check_pin_code(pin_code):
    if len(pin_code) != 4 or not pin_code.isdecimal():
        print_error('Pin code should have length 4 and contain only digits')
    return pin_code
