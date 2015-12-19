## Unzip data file
unzip("exdata-data-NEI_data.zip", overwrite = TRUE)

## Read data.
## It will likely take a few seconds. Be patient!
NEI <- readRDS("summarySCC_PM25.rds")
SCC <- readRDS("Source_Classification_Code.rds")

## Sum total PM2.5 emission from all sources per year respectively
totalpm25 <- aggregate(Emissions ~ year, NEI, sum)

## Make a plot showing the total PM2.5 emission
par(mar=c(6,5,6,5))
plot(totalpm25$year, totalpm25$Emissions / 10^6,
     main = 'Total PM2.5 emission per year',
     xlab = 'year', ylab = expression(paste('PM2.5 emission (',10^6,' Tons)')), 
     type='h', col='blue', lwd=12)
dev.copy(device = png, 'plot1.png')
dev.off()