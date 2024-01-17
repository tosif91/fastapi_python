# fastapi_python

## TODO APP 

1. Create Task 
2. Read Task
3. Update Task
4. Delete Task 
5. Filter Task by ID 
6. Filter Task by Category 


FastAPI is now compatible with both Pydantic v1 and Pydantic v2.

Based on how new the version of FastAPI you are using, there could be small method name changes.



The three biggest are:

.dict() function is now renamed to .model_dump()

schema_extra function within a Config class is now renamed to json_schema_extra

Optional variables need a =None example: id: Optional[int] = None   