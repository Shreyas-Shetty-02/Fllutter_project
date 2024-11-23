from pymongo import MongoClient

client = MongoClient("mongodb+srv://sdsmcollege02:sdsmcollege02@project0.ynyys.mongodb.net/?retryWrites=true&w=majority&appName=Project0")

db = client.Purchase_Inventory

Inventory = db["Inventory"]
Login_Time = db["Login_Time"]
Order_Details = db ["Order_Details"]
