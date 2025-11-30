class Vechicle:
    def __init__(self, make, model):
        self.make = make
        self.model = model
    
    def get_info(self):
        return f"Марка: {self.model}, Модель: {self.model}"

class Car(Vechicle):
    def __init__(self, make, model, fuel_type):
        self.fuel = fuel_type
        super().__init__(make, model)
    def get_info(self):
        car_info = super().get_info()
        return f"{car_info}, Тип топлива: {self.fuel}"

vehicle = Vechicle("BMW", "X5")
car = Car("Toyota", "Camry", "Бензин")

print(vehicle.get_info())
print(car.get_info())