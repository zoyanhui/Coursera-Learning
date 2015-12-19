rankhospital <- function(state, outcome, num="best") {
    ## Read outcome data
    outcomedata <- read.csv("outcome-of-care-measures.csv", 
                          colClasses = "character")
    ## Check that state and outcome are valid
    validstate <- outcomedata[["State"]] == state
    if(sum(validstate) == 0){
      stop("invalid state")
    }
    validstatedata <- outcomedata[validstate, ]
    if(outcome == "heart attack") {
      rankcol <- 11  
    } else if(outcome == "heart failure") {
      rankcol <- 17
    } else if(outcome == "pneumonia") {
      rankcol <- 23
    } else{
      stop("invalid outcome")
    }
    ## Return hospital name in that state with the given rank
    ## 30-day death rate
    testvalcol <- colnames(validstatedata)[rankcol]
    testcolval <- validstatedata[, c("Hospital.Name",testvalcol)]
    testcolval[,testvalcol] <- as.numeric(testcolval[,testvalcol])
    testcolval <- testcolval[complete.cases(testcolval), ]
    len <- nrow(testcolval)
    if(num == "best") {
       num <- 1
    }
    else if(num == "worst") {
       num <- len
    }
    if(len < num){
        return(NA)
    }
    
    bestvalidx <- order(testcolval[,testvalcol], testcolval[,"Hospital.Name"], decreasing = FALSE)
    testcolval[bestvalidx[num], "Hospital.Name"]
}