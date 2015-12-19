library(ggplot2)
## Unzip data file
unzip("exdata-data-NEI_data.zip", overwrite = TRUE)

## Read data.
## It will likely take a few seconds. Be patient!
NEI <- readRDS("summarySCC_PM25.rds")
SCC <- readRDS("Source_Classification_Code.rds")

## Subset dataset for the Baltimore City, Maryland (fips == "24510")
subNEI <- subset(NEI, fips == "24510")
## Sum total PM2.5 emission from all sources per year seperating by type respectively,
## on the subset data
totalpm25_by_type <- aggregate(Emissions ~ year + type, subNEI, sum)

## Make a plot showing the total PM2.5 emission in the Baltimore City
myplot <- qplot(year, Emissions, data=totalpm25_by_type)
myplot <- myplot + aes(color=type)
myplot <- myplot + geom_line()
myplot <- myplot + xlab("year")
myplot <- myplot + ylab("Total PM2.5 emission (Tons)")
myplot <- myplot + ggtitle("PM2.5 emissions in Baltimore city 1999-2008 by source type")
print(myplot)

dev.copy(device = png, 'plot3.png')
dev.off()