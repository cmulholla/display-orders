import time
import json
from flask import Flask, request, jsonify, render_template_string
import requests
import threading

app = Flask(__name__)

# Store orders in a dictionary
orders = {}

@app.route('/')
def home():
    # send the user to the display_orders page
    return display_orders_chrome()

def send_orders_to_server(orders):
    requests.post("http://127.0.0.1:5000/submit_orders", json=orders)

@app.route('/submit_orders', methods=['POST'])
def submit_orders():
    data = request.get_json()
    for order_id, order_details in data.items():
        orders[order_id] = order_details
    return jsonify({"message": "Orders received"}), 200

@app.route('/display_orders')
def display_orders_chrome():
    display_data = []
    for order_id, order_details in orders.items():
        paid_status = "Paid" if "paid" in order_details else "Unpaid"
        order_items = [item for item in order_details if item != "paid"]
        display_data.append({"order_id": order_id, "status": paid_status, "items": order_items})
    
    # Render orders in a simple HTML template
    html_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Customer Orders</title>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            table, th, td {
                border: 1px solid black;
            }
            th, td {
                padding: 10px;
                text-align: left;
            }
            .unpaid {
                color: red;
            }
            .paid {
                color: green;
            }
            #raw_orders {
                display: none;
            }
        </style>
    </head>
    <body>
        <h1>Customer Orders</h1>
        <table>
            <tr>
                <th>Order ID</th>
                <th>Status</th>
                <th>Items</th>
            </tr>
            {% for order in orders %}
            <tr>
                <td>{{ order['order_id'] }}</td>
                <td class="{{ 'unpaid' if order['status'] == 'Unpaid' else 'paid' }}">{{ order['status'] }}</td>
                <td>{{ order['items'] | join(', ') }}</td>
            </tr>
            {% endfor %}
        </table>
        <a id="raw_orders">
            {{ orders }}
        </a>
    </body>
    </html>
    '''

    print("Display data:")
    print(display_data)
    return render_template_string(html_template, orders=display_data)

class CustomerOrders:
    def __init__(self, json_file, order_file):
        self.json_file = json_file
        self.order_file = order_file
        self.load_data()
        self.display_orders()

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
        except OSError:
            print("Error reading file. Creating new file.")
            self.data = {}

    def save_data(self):
        with open(self.json_file, 'w') as file:
            json.dump(self.data, file, indent=4)

    def create_order(self, customer_name, order):
        if customer_name in self.data:
            print(f"Customer {customer_name} already exists.")
        else:
            # remove all ", [, and ] characters from the order
            order = order.replace("', '", ", ").replace("['", "").replace("']", "")
            
            # split the order into a list: "["beef str", "salad"]" -> ["beef str", "salad"]
            order = order.split(", ")

            self.data[customer_name] = order
            self.save_data()
            #print(f"Order for {customer_name} created: {order}")

    def modify_order(self, customer_name, new_order):
        if customer_name in self.data:
            # if new_order is a string instead of a list, then split the string into a list
            if type(new_order) == str:
                new_order = new_order.replace("', '", ", ").replace("['", "").replace("']", "")
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
        #print("\033[H\033[J")
        if len(self.data) == 0:
            print("No orders.")
        for customer, order in self.data.items():
            if order[-1] == "paid":
                order = order[:-1]
                customer = customer + " (paid)"
            strorder = order.__str__().replace("[", "").replace("]", "").replace("'", "")
            print(f"{customer}: {strorder}")
        orders = self.data
        # send the orders to the web server with a post request containing the orders
        send_orders_to_server(orders)


# this class will be used to monitor the file system for changes
class MyHandler():

    def __init__(self):
        self.last_modified = time.time()
        # find the current date and add it to the orders file name
        self.date = time.strftime("%m%d")
        print(f"Watching for changes in orders{self.date}.txt")
        self.orders = CustomerOrders("./json.txt", f"./orders{self.date}.txt")

    def on_modified(self, event):
        current_time = time.time()
        if event.src_path.endswith("orders.txt") and current_time - self.last_modified > 0.01:
            #print(f'{event.src_path} has been modified {current_time - self.last_modified} seconds ago')
            self.last_modified = current_time
            self.retry_load_data()

    def retry_load_data(self, retries=10, delay=0.1):
        if self.date != time.strftime("%m%d"):
            self.date = time.strftime("%m%d")
            self.orders = CustomerOrders("./json.txt", f"./orders{self.date}.txt")
            print(f"Watching for changes in orders{self.date}.txt")
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
    # run the flask app in a separate thread so that the main thread can monitor the file system
    # Create a new thread to run the Flask app
    flask_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000})

    # Start the Flask app thread
    flask_thread.start()

    event_handler = MyHandler()

    # monitor the file system for changes
    try:
        while True:
            time.sleep(10) # sleep for 10 seconds
            # call the retry_load_data function to check if the file has been modified
            event_handler.retry_load_data()

    except KeyboardInterrupt:
        print("Shutting down...")

    # Wait for the Flask app thread to finish
    flask_thread.join(1)
    # Exit the program
    exit(0)
