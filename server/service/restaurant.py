
class Restaurant:
    def __init__(self, id, name, address, longitude, latitude, cuisineGenres=None, dietary=None) -> None:
        self.id=id
        self.name=name
        self.address=address
        self.longitude=longitude
        self.latitude = latitude
        self.cuisineGenres = cuisineGenres
        self.dietary = dietary

    def get_id(self):
        return self.id
    
    def get_location(self):
        return {self.longitude, self.latitude}
    
    def get_cuisineGenres(self):
        return self.cuisineGenres
    
    def get_dietary(self):
        return self.dietary
    
    def dict(self):
        return {
            "name": self.name,
            "address": self.address,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "cuisineGenres": self.cuisineGenres,
            "dietary": self.dietary
        }