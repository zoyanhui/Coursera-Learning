best <- function(state, outcome) {
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
    ## Return hospital name in that state with lowest 30-day death
    ## rate
    testcolval <- as.numeric(validstatedata[, rankcol])
    bestval <- min(testcolval, na.rm = TRUE)
    bestvalindex <- testcolval == bestval
    cadhosp <- validstatedata[bestvalindex, "Hospital.Name"]
    sort(cadhosp)[1]
    
}