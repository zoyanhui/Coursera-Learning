library(shiny)
library(datasets)
data("mtcars")
cyls <- levels(as.factor(mtcars$cyl))
shinyUI(
    pageWithSidebar( 
        headerPanel("Predict Miles/(US) Gallon of Car"), 
        sidebarPanel(    
            
            selectInput(inputId="cyl", label="Number of cylinders", choices=sort(cyls),
                        multiple = FALSE,selected="0"),
            numericInput(inputId="hp", label = "Gross horsepower", value=0, min=0), 
            radioButtons(inputId="am", label="Transmission", choices=c("automatic","manual")),
            textInput(inputId="wt", label = "Weight (lb)"), 
            actionButton("goButton", "Predict")
        ), 
        mainPanel(    
            tabsetPanel(
                tabPanel('Predict Results',
                         h5('Your Inputs:'),                         
                         verbatimTextOutput("cyl"),
                         verbatimTextOutput("hp"),
                         verbatimTextOutput("wt"),
                         verbatimTextOutput("am"),
                         h5("Predict MPG:"),
                         verbatimTextOutput("mpg")                        
                ),
                tabPanel('Documentation',
                         includeMarkdown('help.Rmd'))
            )
        ) 
    )
)