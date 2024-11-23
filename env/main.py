from fastapi import FastAPI
from routes.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(router)


from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://sdsmcollege02:sdsmcollege02@project0.ynyys.mongodb.net/?retryWrites=true&w=majority&appName=Project0"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to specific origins here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

