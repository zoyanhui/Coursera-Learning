pollutantmean <- function(directory, pollutant, id=1:332) {
  ## 'directory' is a character vector of length 1 indicating
  ## the location of the CSV files
  
  ## 'pollutant' is a character vector of length 1 indicating
  ## the name of the pollutant for which we will calculate the
  ## mean; either "sulfate" or "nitrate".
  
  ## 'id' is an integer vector indicating the monitor ID numbers
  ## to be used
  
  ## Return the mean of the pollutant across all monitors list
  ## in the 'id' vector (ignoring NA values)
  ## NOTE: Do not round the result!
  values=vector(mode="numeric")
  for(i in id){
     num <- if(i<10){
        paste("00", as.character(i), sep="")
     }else if(i < 100){
        paste("0", as.character(i), sep="")
     }else{
        as.character(i)
     }
     csvFile <- paste(directory, paste(num, "csv", sep="."), sep="/")
     data <- read.csv(csvFile)
     t <- data[[pollutant]]
     values <- append(values,t[complete.cases(t)])
  }
  mean(values)
  
}