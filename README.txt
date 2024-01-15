# fastapi_python

FastAPI is now compatible with both Pydantic v1 and Pydantic v2.

Based on how new the version of FastAPI you are using, there could be small method name changes.



The three biggest are:

.dict() function is now renamed to .model_dump()

schema_extra function within a Config class is now renamed to json_schema_extra

Optional variables need a =None example: id: Optional[int] = None

* pydantic
# Using pydantic we can apply data validation in on body ,
# Using fatapi we can apply data validation on path  and queryparamters