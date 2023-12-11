import time


max_height = 80
max_width = 80
max_depth = 80
sum = 200
min_weight = 1
max_weight = 10
sum_weight = 0

num_parcel = 1

def get_dimensions():
    global height 
    height = float(input("Pls input height (cm)"))
    global width 
    width = float(input("Pls input width (cm)"))
    global depth 
    depth = float(input("Pls input depth (cm)"))
    global weight 
    weight = float(input("Pls input weight (kg)"))
    validate(height, width, depth, weight)
    
    return height, width, depth, weight

    
    
def validate(height, width, depth, weight):
    if height <= max_height and width <= max_width and depth <= max_depth and weight >= min_weight and weight <= max_weight and height + width + depth <= sum:
        print("Package is valid")
        global x 
        x = "true"
        time.sleep(3)
        more_parcels(x,weight,sum_weight)
    else:
        x = "false"
        print("Package is not valid")
        get_dimensions()
        if height >= max_height:
            print("Package is to long")
            time.sleep(10)
            get_dimensions()
        elif width >= max_width:
            print("Package is to wide")
            time.sleep(10)
            get_dimensions()
        elif depth >= max_depth:
            print("Package is to deep")
            time.sleep(10)
            get_dimensions()
        elif weight < min_weight:
            print("Package is too light")
            time.sleep(10)
            get_dimensions()
        elif weight > max_weight:
            print("Package is too heavy")
            time.sleep(10)
            get_dimensions()
        elif height + width + depth > sum:
            print("Package dimensions exceed sum")
            time.sleep(10)
            get_dimensions()
            

def more_parcels(x,weight,sum_weight):
    if x == "true":
        num_parcel = 0
        more = int(input("Do you have another parcel? 1 for yes, 0 for no: "))
        sum_weight += weight
        
        if more == 1:
            num_parcel += 1
            validate()
            
        elif more == 0:
            
            print(f"{num_parcel} has been successfully added")
            print("The weight of all parcels is:",sum_weight)  
            time.sleep(1)
            calc(sum_weight)
            
        
        
def calc(sum_weight):
    total_cost = 0
    
    
    if sum_weight <= 5 and sum_weight >= 1 :
        print("Your cost is $10")
    elif sum_weight <= 10 and sum_weight >= 5:
        total_cost += 10
        while sum_weight <= 10 and sum_weight >= 5:
            total_cost += 0.1
            sum_weight += 0.1
            
        else:
            print(f"Your cost is {total_cost}")
            
    
    
    
    
    
    
    
    
        
get_dimensions()
            

        
            