class Vehicle:
    def __init__(self, vehicle_id, brand, model, year, price, mileage=0, status="Available"):
        self.vehicle_id = vehicle_id
        self.brand = brand
        self.model = model
        self.year = year 
        self.price = price 
        self.mileage = mileage 
        self.status = status 
        self.owner = None
        
def assign_owner(self, owner_name):
    self.owner = owner_name
    self.status = "Sold"
    
def update_mileage(self, new_mileage):
    self.mileage = new_mileage

def update_status(self, new_status):
    self.status = new_status
    
def update_price(self, new_price):
    self.price = new_price
    
def get_info(self):
    return f"{self.vehicle_id} | {self.brand} | {self.model} | {self.year} | {self.price} Taka | {self.mileage} km | {self.status} | Owner: {self.owner}"


class Car(Vehicle):
    def __init__(self, vehicle_id, brand, model, year, price, doors, mileage=0, status="Available"):
        super().__init__(vehicle_id, brand, model, year, price, doors, mileage, status)
        self.doors = doors
        
    def get_info(self):
        base = super().get_info()
        return f"{base} | Doors: {self.dooors}"
    
    
class Motorcycle(Vehicle):
    def __init__(self, vehicle_id, brand, model, year, price, engine_cc, mileage=0, status="Available"):
        super().__init__(vehicle_id, brand, model, year, price, mileage, status)
        self.engine_cc = engine_cc
        
    def get_info(self):
        base = super().get_info()
        return f"{base} | Engine: {self.engine_cc}cc"
    

class VehicleManager:
    def __init__(self):
        self.cehicles = {}
        
    def add_vechicle(self, vehicle):
        self.
    