library(ggplot2)
## Unzip data file
unzip("exdata-data-NEI_data.zip", overwrite = TRUE)

## Read data.
## It will likely take a few seconds. Be patient!
NEI <- readRDS("summarySCC_PM25.rds")
SCC <- readRDS("Source_Classification_Code.rds")

## Subset dataset for the Baltimore City, Maryland (fips == "24510")
## and Los Angeles County, California (fips == "06037")
subNEI <- subset(NEI, fips %in% c("24510", "06037"))

## Select motor vehicle sources
rows <- which(grepl("vehicle", SCC$SCC.Level.Two, ignore.case=TRUE))
vehicleSCC <- SCC$SCC[rows]
vehicleSet <- subset(subNEI, subNEI$SCC %in% vehicleSCC)

## Calculate vehicle resource emissions
vehicleEmissions <- aggregate(Emissions ~ year + fips, data=vehicleSet, sum)

## plot
vehicleEmissions$city <- "Baltimore City"
vehicleEmissions$city[vehicleEmissions$fips == "06037"] <- "Los Angeles County"
myplot <- qplot(year, Emissions, data=vehicleEmissions)
myplot <- myplot + aes(color=city)
myplot <- myplot + geom_line()
myplot <- myplot + xlab("year")
myplot <- myplot + ylab("PM2.5 emission (Tons)")
myplot <- myplot + ggtitle("PM2.5 motor vehicle resource emissions\n in Baltimore City and Los Angeles County")
print(myplot)

dev.copy(device = png, 'plot6.png')
dev.off()