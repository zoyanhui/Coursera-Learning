rankall <- function(outcome, num="best") {
    ## Read outcome data
    outcomedata <- read.csv("outcome-of-care-measures.csv", 
                          colClasses = "character")
    ## Check that outcome are valid
    if(outcome == "heart attack") {
      rankcol <- 11  
    } else if(outcome == "heart failure") {
      rankcol <- 17
    } else if(outcome == "pneumonia") {
      rankcol <- 23
    } else{
      stop("invalid outcome")
    }
    testvalcol <- colnames(outcomedata)[rankcol]
    testval <- outcomedata[, c("Hospital.Name","State", testvalcol)]
    testval[, testvalcol] <- as.numeric(testval[, testvalcol])
    ## For each state, find the hospital of the given rank
    groupby <- function(idx){
       testval[idx, c("Hospital.Name", testvalcol)]
    }
    groups <- tapply(1:length(testval$State), as.factor(testval$State), groupby)
    rankeach <- function(testdata){
      len <- nrow(testdata)
      if(num == "best") {
        num <- 1
      }
      else if(num == "worst") {
        num <- sum(complete.cases(testdata))
      }
      if(len < num){
        return(NA)
      }
      bestvalidx <- order(testdata[,testvalcol], testdata[,"Hospital.Name"], na.last = TRUE, decreasing = FALSE)
      testdata[bestvalidx[num], "Hospital.Name"]
    }
    rankresult <- lapply(groups, rankeach)
    ## Return a data frame with hospital names and the
    ## (abbreviated) state name
    data.frame(hospital=sapply(rankresult, function(e){e[[1]]}), state=names(rankresult))
    
}