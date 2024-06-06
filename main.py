from fastapi import FastAPI,Depends, status, Response, HTTPException #status for status_code and Response for the response on the status_code
from . import schemas
from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(engine) #once all is done, write this code to start the database and create a table

#-----------------------STARRTING CRUD OPERATIONS----------------------

def get_db():
    db= SessionLocal() #creates a new database session
    try:
        yield db #pause the execution if an exception comes
    finally:
        db.close() #close database

@app.post('/blog' , status_code=status.HTTP_201_CREATED) #we imported status from fastapi so that we can change the status code as we want and don't memorize them
def create(request: schemas.Blog,db: Session= Depends(get_db)): #take parameters (request and db),
                                                                #db will ensure if the database session is available
    new_blog = models.Blog(title=request.title, body=request.body) #import title and body from models.py Blog class
    db.add(new_blog) #create data for table
    db.commit() #add data to database
    db.refresh(new_blog) #refresh database
    return new_blog #return data as an object for the client

@app.get('/blog') #searching all data
def alldata(db: Session= Depends(get_db)): #taking perimeter session
    blogs = db.query(models.Blog).all() #take blogs as variable, assign it. use all() to see all data
    return blogs 

@app.get('/blog/{id}' , status_code=200) #searching one data
def onedata(id,response: Response,db: Session= Depends(get_db)): #taking 2 perimeters(id and session)
    blog = db.query(models.Blog).filter(models.Blog.id==id).first() #take blog as variable, filter and search
                                                                    #on the basis of id and show the first result
    if not blog:
        response.status_code=status.HTTP_404_NOT_FOUND  
        return {'ID NOT FOUND'}                                                              
    return blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def deletion(id,db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return 'DONE'

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request:schemas.Blog, db: Session = Depends(get_db)):
    request_dict = request.dict()
    blog = db.query(models.Blog).filter(models.Blog.id == id).update(request_dict)
    if blog == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} not found")
    db.commit()
    return 'Update Complete'


