from fastapi import HTTPException, status

# 400 Bad Request
badRequestException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Bad request"
)

# 401 Unauthorized
unauthorizedException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid username or password"
)

# 403 Forbidden
forbiddenException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You do not have permission to access this resource"
)

# 404 Not Found
notFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Resource not found"
)

# 409 Conflict
conflictException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Conflict with the current state of the resource"
)

# 422 Unprocessable Entity
unprocessableEntityException = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail="Unprocessable entity"
)

# 500 Internal Server Error
internalServerErrorException = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Internal server error"
)
