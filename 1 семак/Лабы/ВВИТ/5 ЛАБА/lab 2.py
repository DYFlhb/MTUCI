class Circle:
    def __init__(self, radius):
        self.radius = radius
    
    def get_radius(self):
        print(f'Радиус: {self.radius}')
    
    def set_radius(self, new_radius):
        self.radius = new_radius

Circle_A = Circle(15)
Circle_A.set_radius(100)
Circle_A.get_radius() 