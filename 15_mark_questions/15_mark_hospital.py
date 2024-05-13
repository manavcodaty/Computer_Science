patient = ["Bob","Jill","Ben","Grace"]
Readings = [[35.60,56.00],[31.50,55.00],[32.60,101.00],[54.00,101.00]] # Temperature, Pulse

patient_num = int(input("Enter patient number: "))

def hospital(patient_num, pulse = True, temp = True):
    if patient_num < 1 or patient_num > 4: # Checking patient number
        print("Invalid patient number")
    else:
        print("Patient: ", patient[patient_num-1])
        for i in range(len(Readings[patient_num-1])):
            if Readings[patient_num-1][0] >= 37.2 or Readings[patient_num-1][1] <= 31.6:
                print("Warning")
                print("Temperature out of range")
                temp = False
            else:
                print("Temperature is normal")
            if Readings[patient_num-1][1] >= 100 or Readings[patient_num-1][1] <= 55:
                print("Warning")
                print("Pulse out of range")
                pulse = False
            else:
                print("Pulse is normal")
    if pulse == False and temp == False:
        print("Severe Warning")
        print("Temperature and pulse out of range")

hospital(patient_num)


