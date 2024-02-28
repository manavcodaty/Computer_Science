patient = ["Bob", "Jill", "Ben", "Grace"]
Readings = [
    [35.60, 56.00],
    [31.50, 55.00],
    [32.60, 101.00],
    [54.00, 101.00],
]  # Temperature, Pulse
global temp, pulse
temp = True
pulse = True
#            temp, pulse


def hospital(num, pulse, temp):
    if num < 0 or num > 3:  # Checking patient number
        print("Invalid patient number")
    else:
        print("Patient: ", patient[num])
        if Readings[num][0] >= 37.2 or Readings[num][0] <= 31.6:
            print("Warning")
            print("Temperature out of range")
            temp = False
        else:
            print("Temperature is normal")
        if Readings[num][1] >= 100 or Readings[num][1] <= 55:
            print("Warning")
            print("Pulse out of range")
            pulse = False
        else:
            print("Pulse is normal")
    if pulse == False and temp == False:
        print("Severe Warning")
        print("Temperature and pulse out of range")


patient_num = int(input("Enter patient number: "))
num = patient_num - 1
hospital(num, pulse, temp)
