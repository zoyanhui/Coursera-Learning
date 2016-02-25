library(datasets)
data("mtcars")
mtcars$cyl <- factor(mtcars$cyl)
mtcars$am <- factor(mtcars$am, labels = c("automatic", "manual"))
mtcars$gear <- factor(mtcars$gear)
mtcars$carb <- factor(mtcars$carb)
model <- lm(mpg ~ ., data = mtcars)
model <- step(model, trace=FALSE)

shinyServer( 
    function(input, output) {        
        output$cyl <- renderText(paste("cylinders:", {input$cyl})) 
        output$hp <- renderText(paste("horsepower:", {input$hp})) 
        output$wt <- renderText(paste("weight:", {input$wt}, " lb"))
        output$am <- renderText(paste("transmission:", {input$am}))
        output$mpg <- renderText({
            input$goButton
            isolate(pd <- data.frame(input$cyl, input$hp, as.numeric(input$wt)/1000, input$am))
            names(pd) <- c('cyl', 'hp', 'wt', 'am')
            return(paste("Predict:", predict(model, pd)))      
        })
} )