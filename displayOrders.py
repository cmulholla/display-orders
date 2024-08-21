import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json

class CustomerOrders:
    def __init__(self, json_file, order_file):
        self.json_file = json_file
        self.order_file = order_file
        self.load_data()

    def load_data(self):
        operations = 0
        try:
            with open(self.order_file, 'r') as file:
                # go through each line in the file, as the file is not in json format yet
                self.data = {}
                for line in file:
                    operations += 1
                    # if the first word in the line is "create", then create an order
                    if line.split()[0] == "create":
                        self.create_order(line.split()[1], ' '.join(line.split()[2:]))
                    # if the first word in the line is "modify", then modify an order
                    elif line.split()[0] == "modify":
                        self.modify_order(line.split()[1], ' '.join(line.split()[2:]))
                    # if the first word in the line is "delete", then delete an order
                    elif line.split()[0] == "delete":
                        self.delete_order(line.split()[1])
                    # if the first word in the line is "pay", then append the "paid" status to the order
                    elif line.split()[0] == "pay":
                        self.modify_order(line.split()[1], self.data[line.split()[1]] + ["paid"])
                    else:
                        print("Invalid operation: " + line)
                        operations -= 1
            # if self.data contains no data, and the order file is empty, then throw an IOError
            if len(self.data) == 0 and operations == 0:
                raise IOError

        except FileNotFoundError:
            print("File not found. Creating new file.")
            self.data = {}

    def save_data(self):
        with open(self.json_file, 'w') as file:
            json.dump(self.data, file, indent=4)

    def create_order(self, customer_name, order):
        if customer_name in self.data:
            print(f"Customer {customer_name} already exists.")
        else:
            # remove all ", [, and ] characters from the order
            order = order.replace('", "', ", ").replace('["', "").replace('"]', "")
            
            # split the order into a list: "["beef str", "salad"]" -> ["beef str", "salad"]
            order = order.split(", ")

            self.data[customer_name] = order
            self.save_data()
            #print(f"Order for {customer_name} created: {order}")

    def modify_order(self, customer_name, new_order):
        if customer_name in self.data:
            # if new_order is a string instead of a list, then split the string into a list
            if type(new_order) == str:
                new_order = new_order.replace('", "', ", ").replace('["', "").replace('"]', "")
                new_order = new_order.split(", ")
            self.data[customer_name] = new_order
            self.save_data()
            #print(f"Order for {customer_name} modified: {self.data}")
        else:
            print(f"Customer {customer_name} does not exist.")

    def delete_order(self, customer_name):
        if customer_name in self.data:
            del self.data[customer_name]
            self.save_data()
            #print(f"Order for {customer_name} deleted.")
        else:
            print(f"Customer {customer_name} does not exist.")
    
    def display_orders(self):
        print("Orders:")
        # clear the console using ANSI escape codes (black magic given to me by copilot)
        print("\033[H\033[J")
        if len(self.data) == 0:
            print("No orders.")
        for customer, order in self.data.items():
            if order[-1] == "paid":
                order = order[:-1]
                customer = customer + " (paid)"
            strorder = order.__str__().replace("[", "").replace("]", "").replace("'", "")
            print(f"{customer}: {strorder}")

# this class will be used to monitor the file system for changes
class MyHandler(FileSystemEventHandler):

    def __init__(self):
        self.last_modified = time.time()
        self.orders = CustomerOrders("./json.txt", "./orders.txt")

    def on_modified(self, event):
        current_time = time.time()
        if event.src_path.endswith("orders.txt") and current_time - self.last_modified > 0.01:
            #print(f'{event.src_path} has been modified {current_time - self.last_modified} seconds ago')
            self.last_modified = current_time
            self.retry_load_data()

    def retry_load_data(self, retries=10, delay=0.1):
        for _ in range(retries):
            try:
                self.orders.load_data()
                self.orders.display_orders()
                break
            except IOError:
                #print("File is busy, retrying...")
                time.sleep(delay)

if __name__ == "__main__":
    path = "."  # Directory to watch
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)

    observer.start()

    # Write to "test.txt" to trigger the event
    with open("test.txt", "w") as file:
        file.write("Hello, World!")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()