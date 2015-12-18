complete <- function(directory, id = 1:332) {
  ## 'directory' is a character vector of length 1 indicating
  ## the location of the CSV files
  
  ## 'id' is an integer vector indicating the monitor ID numbers
  ## to be used
  
  ## Return a data frame of the form:
  ## id nobs
  ## 1  117
  ## 2  1041
  ## ...
  ## where 'id' is the monitor ID number and 'nobs' is the
  ## number of complete cases
  goods = vector()
  for(i in id){
    num <- if(i<10){
      paste("00", as.character(i), sep="")
    }else if(i < 100){
      paste("0", as.character(i), sep="")
    }else{
      as.character(i)
    }
    csvFile <- paste(directory, paste(num, "csv", sep="."), sep="/")
    d <- read.csv(csvFile)
    good <- complete.cases(d)
    c <- d[good,]
    goods <- append(goods, nrow(c))
  }
  data.frame(id = id, nobs = goods)
}