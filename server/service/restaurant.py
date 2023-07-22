
class Restaurant:
    def __init__(self, id, name, address, longitude, latitude) -> None:
        self.id=id
        self.name=name
        self.address=address
        self.longitude=longitude
        self.latitude = latitude
    
    def get_id(self):
        return self.id
    
    def get_location(self):
        return {self.longitude, self.latitude}
    
    def dict(self):
        return {
            "name": self.name,
            "address": self.address,
            "longitude": self.longitude,
            "latitude": self.latitude
        }