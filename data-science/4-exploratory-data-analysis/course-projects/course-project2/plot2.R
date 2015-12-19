## Unzip data file
unzip("exdata-data-NEI_data.zip", overwrite = TRUE)

## Read data.
## It will likely take a few seconds. Be patient!
NEI <- readRDS("summarySCC_PM25.rds")
SCC <- readRDS("Source_Classification_Code.rds")

## Subset dataset for the Baltimore City, Maryland (fips == "24510")
subNEI <- subset(NEI, fips == "24510")
## Sum total PM2.5 emission from all sources per year respectively,
## on the subset data
totalpm25 <- aggregate(Emissions ~ year, subNEI, sum)

## Make a plot showing the total PM2.5 emission in the Baltimore City
par(mar=c(6,5,6,5))
plot(totalpm25$year, totalpm25$Emissions / 10^3,
     main = 'PM2.5 emission in the Baltimore City, Maryland ',
     xlab = 'year', ylab = expression(paste('PM2.5 emission (',10^3,' Tons)')), 
     type='h', col='blue', lwd=12)
dev.copy(device = png, 'plot2.png')
dev.off()