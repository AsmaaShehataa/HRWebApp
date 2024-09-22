class Vehicle:
    def __init__(self, name):
        self.name = name

    def get_type(self):
        raise NotImplementedError("Subclasses should implement this method!")

class Car(Vehicle):
    def get_type(self):
        return "Car"


# Factory DP - factory method 

class VehicleFactory:
    def get_vehicle(vehicle_type, name):
        if vehicle_type == "Car":
            return Car(name)
        else:
            raise ValueError(f"Unknown car type: {vehicle_type}")


if __name__ == '__main__':
    vehicle_type = input("Enter vehicle type (Car, Truck, Bike): ")
    vehicle_name = input("Enter your vehicle Name: ")
    
    vehicle = VehicleFactory.get_vehicle(vehicle_type, vehicle_name)
    print(f"Vehicle type: {vehicle.get_type()}")
    print(f"Vehicle name: {vehicle.name}")
    
