## Unzip data file
unzip("exdata-data-NEI_data.zip", overwrite = TRUE)

## Read data.
## It will likely take a few seconds. Be patient!
NEI <- readRDS("summarySCC_PM25.rds")
SCC <- readRDS("Source_Classification_Code.rds")

## Subset dataset for the Baltimore City, Maryland (fips == "24510")
subNEI <- subset(NEI, fips == "24510")

## Select motor vehicle sources
rows <- which(grepl("vehicle", SCC$SCC.Level.Two, ignore.case=TRUE))
vehicleSCC <- SCC$SCC[rows]
vehicleSet <- subset(subNEI, subNEI$SCC %in% vehicleSCC)

## Calculate vehicle resource emissions
vehicleEmissions <- aggregate(Emissions ~ year, data=vehicleSet, sum)

## plot
par(mar=c(6,5,6,5))
plot(vehicleEmissions$year, vehicleEmissions$Emissions, 
     xlab = 'year', ylab = expression(paste('PM2.5 emission (Tons)')), 
     main='PM2.5 motor vehicle resource emissions in Baltimore City',
     type='h', col='blue' , lwd=12, cex.main=1)
dev.copy(device = png, 'plot5.png')
dev.off()