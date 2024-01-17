from pydantic import BaseModel,Field
#for data validation we will use this class once the validation is passed then only
#data will be  written in the database
#we are not passing id here as it will automatically added by sqlalchemy
class TodoRequest(BaseModel):
    title: str = Field(min_length=3,max_length=50,description='should be minimum of 3')
    description: str = Field(min_length=5,max_length=100,description='should be max of 100')
    priority: int = Field(ge=1,le=5, description='should be greater then 0',)
    complete: bool
