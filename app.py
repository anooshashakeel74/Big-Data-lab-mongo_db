import os
from datetime import datetime
from bson import ObjectId
from mongo import MongoDB
from dotenv import load_dotenv

load_dotenv()

class InventorySystem:
    def __init__(self):
        self.db = MongoDB()
        self.collection = None
        
    def initialize_database(self):
        if self.db.connect():
            self.collection = self.db.get_collection()
            return True
        return False
    
    def calculate_total_price(self, unit_price, quantity):
        return unit_price * quantity
    
    def create_product(self, serial_number, name, unit_price, quantity):
        try:
            if self.collection.find_one({"serial_number": serial_number}):
                print("Product with this serial number already exists!")
                return False
            
            total_price = self.calculate_total_price(unit_price, quantity)
            
            product = {
                "serial_number": serial_number,
                "name": name,
                "unit_price": unit_price,
                "quantity": quantity,
                "total_price": total_price,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
            
            result = self.collection.insert_one(product)
            print(f"✅ Product '{name}' added successfully with ID: {result.inserted_id}")
            return True
            
        except Exception as e:
            print(f"Error creating product: {e}")
            return False
    
    def read_all_products(self):
        """Read all products from inventory"""
        try:
            products = list(self.collection.find())
            
            if not products:
                print("No products found in inventory!")
                return []
            
            print("\n" + "="*80)
            print("INVENTORY PRODUCTS")
            print("="*80)
            
            for product in products:
                print(f"ID: {product['_id']}")
                print(f"Serial Number: {product['serial_number']}")
                print(f"Name: {product['name']}")
                print(f"Unit Price: ${product['unit_price']:.2f}")
                print(f"Quantity: {product['quantity']}")
                print(f"Total Price: ${product['total_price']:.2f}")
                print(f"Last Updated: {product['updated_at'].strftime('%Y-%m-%d %H:%M:%S')}")
                print("-" * 40)
            
            return products
            
        except Exception as e:
            print(f"Error reading products: {e}")
            return []
    
    def read_product(self, serial_number):
        try:
            product = self.collection.find_one({"serial_number": serial_number})
            
            if not product:
                print("Product not found!")
                return None
            
            print("\n" + "="*50)
            print("PRODUCT DETAILS")
            print("="*50)
            print(f"ID: {product['_id']}")
            print(f"Serial Number: {product['serial_number']}")
            print(f"Name: {product['name']}")
            print(f"Unit Price: ${product['unit_price']:.2f}")
            print(f"Quantity: {product['quantity']}")
            print(f"Total Price: ${product['total_price']:.2f}")
            print(f"Last Updated: {product['updated_at'].strftime('%Y-%m-%d %H:%M:%S')}")
            
            return product
            
        except Exception as e:
            print(f"Error reading product: {e}")
            return None
    
    def update_product(self, serial_number, name=None, unit_price=None, quantity=None):
        try:
            product = self.collection.find_one({"serial_number": serial_number})
            
            if not product:
                print("Product not found!")
                return False
            
            update_data = {"updated_at": datetime.now()}
            
            if name:
                update_data["name"] = name
            
            if unit_price is not None:
                update_data["unit_price"] = unit_price
            
            if quantity is not None:
                update_data["quantity"] = quantity
            
            if unit_price is not None or quantity is not None:
                new_unit_price = unit_price if unit_price is not None else product['unit_price']
                new_quantity = quantity if quantity is not None else product['quantity']
                update_data["total_price"] = self.calculate_total_price(new_unit_price, new_quantity)
            
            result = self.collection.update_one(
                {"serial_number": serial_number},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                print("Product updated successfully!")
                return True
            else:
                print("No changes made to the product.")
                return False
                
        except Exception as e:
            print(f"Error updating product: {e}")
            return False
    
    def delete_product(self, serial_number):
        try:
            result = self.collection.delete_one({"serial_number": serial_number})
            
            if result.deleted_count > 0:
                print("Product deleted successfully!")
                return True
            else:
                print("Product not found!")
                return False
                
        except Exception as e:
            print(f"Error deleting product: {e}")
            return False
    
    def get_inventory_summary(self):
        try:
            products = list(self.collection.find())
            
            if not products:
                print("No products in inventory!")
                return
            
            total_inventory_value = sum(product['total_price'] for product in products)
            total_products = len(products)
            total_quantity = sum(product['quantity'] for product in products)
            
            print("\n" + "="*50)
            print("INVENTORY SUMMARY")
            print("="*50)
            print(f"Total Products: {total_products}")
            print(f"Total Quantity: {total_quantity}")
            print(f"Total Inventory Value: ${total_inventory_value:.2f}")
            print("="*50)
            
        except Exception as e:
            print(f"Error getting inventory summary: {e}")
    
    def display_menu(self):
        
        print("\n" + "="*50)
        print("INVENTORY MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Add New Product")
        print("2. View All Products")
        print("3. Find Product by Serial Number")
        print("4. Update Product")
        print("5. Delete Product")
        print("6. Inventory Summary")
        print("7. Exit")
        print("="*50)
    
    def run(self):
        if not self.initialize_database():
            print("Failed to connect to database. Exiting...")
            return
        
        print("Inventory System Started Successfully!")
        
        while True:
            self.display_menu()
            
            try:
                choice = input("\nEnter your choice (1-7): ").strip()
                
                if choice == '1':
                    print("\n ADD NEW PRODUCT")
                    serial_number = input("Enter Serial Number: ").strip()
                    name = input("Enter Product Name: ").strip()
                    unit_price = float(input("Enter Unit Price: "))
                    quantity = int(input("Enter Quantity: "))
                    self.create_product(serial_number, name, unit_price, quantity)
                
                elif choice == '2':
                    self.read_all_products()
                
                elif choice == '3':
                    print("\n FIND PRODUCT")
                    serial_number = input("Enter Serial Number: ").strip()
                    self.read_product(serial_number)
                
                elif choice == '4':
                    print("\n UPDATE PRODUCT")
                    serial_number = input("Enter Serial Number of product to update: ").strip()
                    
                    print("Leave field empty to keep current value:")
                    name = input("Enter New Name (or press Enter to skip): ").strip()
                    name = name if name else None
                    
                    unit_price_input = input("Enter New Unit Price (or press Enter to skip): ").strip()
                    unit_price = float(unit_price_input) if unit_price_input else None
                    
                    quantity_input = input("Enter New Quantity (or press Enter to skip): ").strip()
                    quantity = int(quantity_input) if quantity_input else None
                    
                    self.update_product(serial_number, name, unit_price, quantity)
                
                elif choice == '5':
                    print("\n DELETE PRODUCT")
                    serial_number = input("Enter Serial Number of product to delete: ").strip()
                    confirm = input(f"Are you sure you want to delete product {serial_number}? (y/n): ").strip().lower()
                    if confirm == 'y':
                        self.delete_product(serial_number)
                    else:
                        print(" Deletion cancelled.")
                
                elif choice == '6':
                    self.get_inventory_summary()
                
                elif choice == '7':
                    print("Thank you for using Inventory Management System!")
                    self.db.close()
                    break
                
                else:
                    print("Invalid choice! Please enter a number between 1-7.")
            
            except ValueError:
                print("Invalid input! Please enter valid data.")
            except KeyboardInterrupt:
                print("\n Program interrupted by user. Exiting...")
                self.db.close()
                break
            except Exception as e:
                print(f" An error occurred: {e}")

if __name__ == "__main__":
    inventory_system = InventorySystem()
    inventory_system.run()