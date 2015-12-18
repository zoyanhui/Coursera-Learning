corr <- function(directory, threshold = 0) {
  ## 'directory' is a character vector of length 1 indicating
  ## the location of the CSV files
  
  ## 'threshold' is a numeric vector of length 1 indicating the
  ## number of completely observed observations (on all
  ## variables) required to compute the correlation between
  ## nitrate and sulfate; the default is 0
  
  ## Return a numeric vector of correlations
  ## NOTE: Do not round the result!
  goods <- complete(directory)
  id <- goods[goods[['nobs']] > threshold, 'id']
  #sulfate <- vector()
  #nitrate <- vector()
  result <- vector(mode="numeric", length=0)
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
    #sulfate <- append(sulfate, c[['sulfate']])
    #nitrate <- append(nitrate, c[['nitrate']])
    cr <- cor(c[["sulfate"]], c[["nitrate"]])
    result <- append(result, cr)
  }
  #cor(sulfate, nitrate)
  result
}