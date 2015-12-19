## Unzip data file
unzip("exdata-data-NEI_data.zip", overwrite = TRUE)

## Read data.
## It will likely take a few seconds. Be patient!
NEI <- readRDS("summarySCC_PM25.rds")
SCC <- readRDS("Source_Classification_Code.rds")

## Select coal combustion-related resource
rows <- which(grepl('combustion', SCC$SCC.Level.One, ignore.case = TRUE) &
    grepl('coal', SCC$SCC.Level.Four, ignore.case = TRUE))
coalCombSCC <- SCC$SCC[rows]
coalCombSet <- subset(NEI, NEI$SCC %in% coalCombSCC)

## Sum all coal combustion-related resource emissions per year
coalCombEmissions <- aggregate(Emissions ~ year, data=coalCombSet, sum)

## plot
par(mar=c(6,5,6,5))
plot(coalCombEmissions$year, coalCombEmissions$Emissions/10^5, 
     xlab = 'year', ylab = expression(paste('PM2.5 emission (',10^5,' Tons)')), 
     main='Coal combustion-related resource emissions',
     type='h', col='blue' , lwd=12)
dev.copy(device = png, 'plot4.png')
dev.off()