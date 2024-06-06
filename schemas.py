from pydantic import BaseModel
#this file contains the data that will be put in the table. There are the perimeters used to input data
class Blog(BaseModel):
    title:str
    body:str
