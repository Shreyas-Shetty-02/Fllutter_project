from fastapi import APIRouter, Response
from pydantic import BaseModel, EmailStr
from config.database import Inventory, Login_Time,Order_Details
from bson import ObjectId
import datetime
import csv
from fastapi.responses import StreamingResponse
from io import StringIO
# from fastapi import HTTPException


router = APIRouter()

# Define Pydantic models for the request body
class RegisterRequest(BaseModel):
    name: str
    email: EmailStr  # Use EmailStr for email validation
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AddChemicalDetailRequest(BaseModel):
    name:str
    grade:str
    rate:float
    quantity:int
    total_cost:float
    discounted_cost:float
    date_of_order:str
    date_of_delivery:str
    remarks:str
    department:str
    email:str
    password:str

class AddInstrumentDetailRequest(BaseModel):
    name:str
    warranty:str
    rate:float
    quantity:int
    total_cost:float
    discounted_cost:float
    date_of_order:str
    date_of_delivery:str
    remarks:str
    department:str
    email:str
    password:str

class AddGlasswareDetailRequest(BaseModel):
    name:str
    capacity:int
    rate:float
    quantity:int
    total_cost:float
    discounted_cost:float
    date_of_order:str
    date_of_delivery:str
    remarks:str
    department:str
    email:str
    password:str

class AddSoftwareDetailRequest(BaseModel):
    name:str
    company_specification:str
    total_cost:float
    discounted_cost:float
    date_of_order:str
    date_of_delivery:str
    remarks:str
    department:str
    email:str
    password:str

class AddTeachingAidsDetailRequest(BaseModel):
    name:str
    type_of_aids:str
    rate:float
    quantity:int
    total_cost:float
    discounted_cost:float
    date_of_order:str
    date_of_delivery:str
    remarks:str
    department:str
    email:str
    password:str

class GetDepartmentDetails(BaseModel):
    email:str
    password:str
    department:str
    type:str

class GetCSVDetails(BaseModel):
    email:str
    password:str
    department:str
    type:str

# class DeleteRequest(BaseModel):
#     email: str
#     password: str
#     department: str
#     type: str
#     entry_id: str


# Register endpoint with Pydantic model
@router.post("/register")
async def accept_register_new_user(request: RegisterRequest, res: Response):
    res.headers.append("Access-Control-Allow-Origin", "*")
    person = Inventory.find_one({"email": request.email})
    if person is None:
        id = ObjectId()
        Inventory.insert_one({
            "_id": id,
            "name": request.name,
            "email": request.email,
            'password': request.password
        })
        res.status_code = 200
        return {"message": "Registered successfully"}
    else:
        res.status_code = 404
        return {"message": "Person already registered"}

# Login endpoint with Pydantic model
@router.post("/login")
async def login(request: LoginRequest, res: Response):
    res.headers.append("Access-Control-Allow-Origin", "*")
    new_email = Inventory.find_one({
        "email": request.email,
        "password": request.password
    })
    if new_email is None:
        res.status_code = 404
        return {"message": "Please check your email and password"}
    else:
        res.status_code = 200
        Login_Time.insert_one({
            "email": request.email,
            'password': request.password,
            "time": datetime.datetime.now()
        })
        return {"message": "Login successful"}

@router.post("/add_chemical_details")
async def Detail(request: AddChemicalDetailRequest, res: Response):
    res.headers.append("Access-Control-Allow-Origin", "*")
    user = Inventory.find_one({
        "email": request.email,
        "password": request.password
    })
    if user is None:
        res.status_code = 404
        return {"message": "User not found"}
    else:
        res.status_code = 200
        Order_Details.insert_one({
            "name":request.name,
            "grade":request.grade,
            "rate":request.rate,
            "quantity":request.quantity,
            "total_cost":request.total_cost,
            "discounted_cost":request.discounted_cost,
            "date_of_order": datetime.datetime.fromisoformat( request.date_of_order),
            "date_of_delivery": datetime.datetime.fromisoformat( request.date_of_delivery),
            "remarks":request.remarks,
            "ordered_by":request.email,
            "type":"chemical",
            "department":request.department,
        })
        return {"message": "Date added successfully"}

@router.post("/get_details")
async def Detail(request: GetDepartmentDetails, res: Response):
    res.headers.append("Access-Control-Allow-Origin", "*")
    user = Inventory.find_one({
        "email": request.email,
        "password": request.password
    })
    if user is None:
        res.status_code = 404
        return {"message": "User not found"}
    else:
        res.status_code = 200
        details = Order_Details.find({
            "department":request.department,
            "type":request.type,
            "ordered_by":request.email,
        },{"_id":0})
        n = 0
        new_details = []
        for i in details:
            i["id"] = n
            new_details.append(i)
            n+=1
        print(new_details)
        return {"details": new_details}

@router.post("/add_instrument_details")
async def Detail(request: AddInstrumentDetailRequest, res: Response):
    res.headers.append("Access-Control-Allow-Origin", "*")
    user = Inventory.find_one({
        "email": request.email,
        "password": request.password
    })
    if user is None:
        res.status_code = 404
        return {"message": "User not found"}
    else:
        res.status_code = 200
        Order_Details.insert_one({
            "name":request.name,
            "warranty":request.warranty,
            "rate":request.rate,
            "quantity":request.quantity,
            "total_cost":request.total_cost,
            "discounted_cost":request.discounted_cost,
            "date_of_order": datetime.datetime.fromisoformat( request.date_of_order),
            "date_of_delivery": datetime.datetime.fromisoformat( request.date_of_delivery),
            "remarks":request.remarks,
            "ordered_by":request.email,
            "type":"instrument",
            "department":request.department,
        })
        return {"message": "Date added successfully"}

@router.post("/add_glassware_details")
async def Detail(request: AddGlasswareDetailRequest, res: Response):
    res.headers.append("Access-Control-Allow-Origin", "*")
    user = Inventory.find_one({
        "email": request.email,
        "password": request.password
    })
    if user is None:
        res.status_code = 404
        return {"message": "User not found"}
    else:
        res.status_code = 200
        Order_Details.insert_one({
            "name":request.name,
            "capacity":request.capacity,
            "rate":request.rate,
            "quantity":request.quantity,
            "total_cost":request.total_cost,
            "discounted_cost":request.discounted_cost,
            "date_of_order": datetime.datetime.fromisoformat( request.date_of_order),
            "date_of_delivery": datetime.datetime.fromisoformat( request.date_of_delivery),
            "remarks":request.remarks,
            "ordered_by":request.email,
            "type":"glassware",
            "department":request.department,
        })
        return {"message": "Date added successfully"}

@router.post("/add_software_details")
async def Detail(request: AddSoftwareDetailRequest, res: Response):
    res.headers.append("Access-Control-Allow-Origin", "*")
    user = Inventory.find_one({
        "email": request.email,
        "password": request.password
    })
    if user is None:
        res.status_code = 404
        return {"message": "User not found"}
    else:
        res.status_code = 200
        Order_Details.insert_one({
            "name":request.name,
            "company_specification":request.company_specification,
            "total_cost":request.total_cost,
            "discounted_cost":request.discounted_cost,
            "date_of_order": datetime.datetime.fromisoformat( request.date_of_order),
            "date_of_delivery": datetime.datetime.fromisoformat( request.date_of_delivery),
            "remarks":request.remarks,
            "ordered_by":request.email,
            "type":"software",
            "department":request.department,
        })
        return {"message": "Date added successfully"}

@router.post("/add_teaching_aids_details")
async def Detail(request: AddTeachingAidsDetailRequest, res: Response):
    res.headers.append("Access-Control-Allow-Origin", "*")
    user = Inventory.find_one({
        "email": request.email,
        "password": request.password
    })
    if user is None:
        res.status_code = 404
        return {"message": "User not found"}
    else:
        res.status_code = 200
        Order_Details.insert_one({
            "name":request.name,
            "type_of_aids":request.type_of_aids,
            "rate":request.rate,
            "quantity":request.quantity,
            "total_cost":request.total_cost,
            "discounted_cost":request.discounted_cost,
            "date_of_order": datetime.datetime.fromisoformat( request.date_of_order),
            "date_of_delivery": datetime.datetime.fromisoformat( request.date_of_delivery),
            "remarks":request.remarks,
            "ordered_by":request.email,
            "type":"teaching_aids",
            "department":request.department,
        })
        return {"message": "Date added successfully"}



@router.post("/export_csv")
async def export_csv(request: GetCSVDetails, res: Response):
    res.headers.append("Access-Control-Allow-Origin", "*")

    user = Inventory.find_one({
        "email": request.email,
        "password": request.password
    })

    if user is None:
        res.status_code = 404
        return {"message": "User not found"}
    else:
        # Fetch the order details based on the department, type, and email
        details = Order_Details.find({
            "department": request.department,
            "type": request.type,
            "ordered_by": request.email
        }, {"_id": 0})

        # Create a StringIO object to store CSV data
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)

        # Write the header dynamically based on the type
        if request.type == "chemical":
            writer.writerow(["Name", "Grade", "Rate", "Quantity", "Total Cost", 
                             "Discounted Cost", "Date of Order", "Date of Delivery", "Remarks"])
        elif request.type == "instrument":
            writer.writerow(["Name", "Warranty", "Rate", "Quantity", "Total Cost", 
                             "Discounted Cost", "Date of Order", "Date of Delivery", "Remarks"])
        elif request.type == "glassware":
            writer.writerow(["Name", "Capacity", "Rate", "Quantity", "Total Cost", 
                             "Discounted Cost", "Date of Order", "Date of Delivery", "Remarks"])
        elif request.type == "software":
            writer.writerow(["Name", "Company Specification", "Total Cost", 
                             "Discounted Cost", "Date of Order", "Date of Delivery", "Remarks"])
        elif request.type == "teaching_aids":
            writer.writerow(["Name", "Type of Aids", "Rate", "Quantity", "Total Cost", 
                             "Discounted Cost", "Date of Order", "Date of Delivery", "Remarks"])

        # Write each row based on the type
        for detail in details:
            if request.type == "chemical":
                writer.writerow([
                    detail.get("name"),
                    detail.get("grade", ""),
                    detail.get("rate", ""),
                    detail.get("quantity", ""),
                    detail.get("total_cost", ""),
                    detail.get("discounted_cost", ""),
                    detail.get("date_of_order").strftime('%Y-%m-%d') if detail.get("date_of_order") else "",
                    detail.get("date_of_delivery").strftime('%Y-%m-%d') if detail.get("date_of_delivery") else "",
                    detail.get("remarks", "")
                ])
            elif request.type == "instrument":
                writer.writerow([
                    detail.get("name"),
                    detail.get("warranty", ""),
                    detail.get("rate", ""),
                    detail.get("quantity", ""),
                    detail.get("total_cost", ""),
                    detail.get("discounted_cost", ""),
                    detail.get("date_of_order").strftime('%Y-%m-%d') if detail.get("date_of_order") else "",
                    detail.get("date_of_delivery").strftime('%Y-%m-%d') if detail.get("date_of_delivery") else "",
                    detail.get("remarks", "")
                ])
            elif request.type == "glassware":
                writer.writerow([
                    detail.get("name"),
                    detail.get("capacity", ""),
                    detail.get("rate", ""),
                    detail.get("quantity", ""),
                    detail.get("total_cost", ""),
                    detail.get("discounted_cost", ""),
                    detail.get("date_of_order").strftime('%Y-%m-%d') if detail.get("date_of_order") else "",
                    detail.get("date_of_delivery").strftime('%Y-%m-%d') if detail.get("date_of_delivery") else "",
                    detail.get("remarks", "")
                ])
            elif request.type == "software":
                writer.writerow([
                    detail.get("name"),
                    detail.get("company_specification", ""),
                    detail.get("total_cost", ""),
                    detail.get("discounted_cost", ""),
                    detail.get("date_of_order").strftime('%Y-%m-%d') if detail.get("date_of_order") else "",
                    detail.get("date_of_delivery").strftime('%Y-%m-%d') if detail.get("date_of_delivery") else "",
                    detail.get("remarks", "")
                ])
            elif request.type == "teaching_aids":
                writer.writerow([
                    detail.get("name"),
                    detail.get("type_of_aids", ""),
                    detail.get("rate", ""),
                    detail.get("quantity", ""),
                    detail.get("total_cost", ""),
                    detail.get("discounted_cost", ""),
                    detail.get("date_of_order").strftime('%Y-%m-%d') if detail.get("date_of_order") else "",
                    detail.get("date_of_delivery").strftime('%Y-%m-%d') if detail.get("date_of_delivery") else "",
                    detail.get("remarks", "")
                ])

        # Set up the response for the CSV file download
        csv_buffer.seek(0)
        response = StreamingResponse(csv_buffer, media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=order_details.csv"
        return response



# @router.post("/software_export_csv")
# async def export_csv(request: GetCSVDetails, res: Response):
#     res.headers.append("Access-Control-Allow-Origin", "*")
    
#     user = Inventory.find_one({
#         "email": request.email,
#         "password": request.password
#     })
    
#     if user is None:
#         res.status_code = 404
#         return {"message": "User not found"}
#     else:
#         # Fetch the order details based on the department, type, and email
#         details = Order_Details.find({
#             "department": request.department,
#             "type": request.type,
#             "ordered_by": request.email
#         }, {"_id": 0})
        
#         # Create a StringIO object to store CSV data
#         csv_buffer = StringIO()
#         writer = csv.writer(csv_buffer)

#         # Write the header for the CSV file
#         writer.writerow(["Name", "company_specification", "Total Cost", 
#                          "Discounted Cost", "Date of Order", "Date of Delivery", "Remarks"])

#         # Write each detail to the CSV
#         for detail in details:
#             writer.writerow([
                
#                 detail.get("name"),
#                 detail.get("grade") or detail.get("type_of_aids") or detail.get("company_specification") or detail.get("capacity")or detail.get("warranty"),
#                 detail.get("total_cost", ""),
#                 detail.get("discounted_cost", ""),
#                 detail.get("date_of_order").strftime('%Y-%m-%d') if detail.get("date_of_order") else "",
#                 detail.get("date_of_delivery").strftime('%Y-%m-%d') if detail.get("date_of_delivery") else "",
#                 detail.get("remarks", "")
#             ])

#         # Set up the response for the CSV file download
#         csv_buffer.seek(0)
#         response = StreamingResponse(csv_buffer, media_type="text/csv")
#         response.headers["Content-Disposition"] = "attachment; filename=order_details.csv"
#         return response
# @router.delete("/delete_entry")
# async def delete_entry(request: DeleteRequest, res: Response):
#     res.headers.append("Access-Control-Allow-Origin", "*")
    
#     # Verify user credentials
#     user = Inventory.find_one({
#         "email": request.email,
#         "password": request.password
#     })
    
#     if user is None:
#         res.status_code = 404
#         return {"message": "User not found"}
    
#     # Convert entry_id to ObjectId
#     try:
#         entry_id = ObjectId(request.entry_id)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail="Invalid entry ID format")

#     # Delete the record
#     result = Order_Details.delete_one({
#         "_id": entry_id,
#         "department": request.department,
#         "type": request.type,
#         "ordered_by": request.email
#     })
    
#     if result.deleted_count == 0:
#         res.status_code = 404
#         return {"message": "Entry not found or unauthorized deletion attempt"}
    
#     res.status_code = 200
#     return {"message": "Entry deleted successfully"}