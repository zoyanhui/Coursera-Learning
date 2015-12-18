## The Following Two function solve inverse of matrix, and 
## cache the inverse. So, it's benefit to save time for repeatedly
## computing costly matrix inverse.

## Function makeCacheMatrix creates a special "matrix" object
## that can cache its inverse.
makeCacheMatrix <- function(m = matrix()) {
    inverseMatrix <- NULL
    set <- function(matrixV){
        m <<- matrixV
        inverseMatrix <<- NULL
    }
    get <- function() m
    setinverse <- function(inverseM){
        inverseMatrix <<- inverseM
    }
    getinverse <- function() inverseMatrix
    list(get = get, set = set, 
         getinverse = getinverse,
         setinverse = setinverse)
}


## Function cacheSolve compute the inverse of the specail "matrix"
## created by function makeCacheMatrix.
## If the inverse has been computed(special "matrix"'s inverseMatrix is not NULL),
## just retrieve the cached inverse.
cacheSolve <- function(x, ...) {
    ## Return a matrix that is the inverse of 'x'
    inverseM <- x$getinverse()
    if(!is.null(inverseM)){
        message("get cached data")
        return(inverseM)
    }
    matrixV <- x$get()
    inverseM <- solve(matrixV)
    x$setinverse(inverseM)
    inverseM
}
