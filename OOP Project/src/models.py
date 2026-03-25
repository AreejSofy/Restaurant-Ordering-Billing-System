class menu:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

class Order:
    def __init__(self):
        self.items = []
        
    def add_item(self, item):
        self.items.append(item)
        
    def remove_item(self, item_name):
        for i in range(len(self.items) - 1, -1, -1):
            if self.items[i].name == item_name:
                self.items.pop(i)
                return True
        return False
        
    def item_count(self):
        return len(self.items)
        
    def clear(self):
        self.items.clear()
        
    def calculate_total(self):
        return sum(item.price for item in self.items)