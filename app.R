#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(shinythemes)
library(shinyWidgets)
library(randomForest)
library(data.table)
library(DT)
library(vader)

library(reticulate)

# Define any Python packages needed for the app here:
PYTHON_DEPENDENCIES = c('numpy', 'pandas', 'matplotlib', 'wbgapi', 'urllib3')

#use_condaenv("Indicateurs", required = TRUE)



#Read Dataset

weather <- read.csv("data/weather-weka.csv", stringsAsFactors = TRUE)

#Build model
model <- randomForest(play~., data=weather, ntree = 500, mtry=4, importance=TRUE)

#Let's save the model to RDS file
saveRDS(model, file = "data/model.rds")

#Let's load the model previously saved
model <- readRDS("data/model.rds")


# Define UI for application that draws a histogram
ui <- fluidPage(
  theme = shinytheme("united"),
  
  

    # Application title
    #titlePanel("Would you Play Golf?"),
    navbarPage(title = "Set of Predictions using R Shiny",
        tabPanel(title = "Play Golf Prediction",
                 setBackgroundImage(
                   src = "images.png"
                 ), 
                 sidebarLayout(
                   sidebarPanel(
                     tags$h3("Input parameters"),
                     selectInput(inputId = "outlook", 
                                 label = "Outlook",
                                 choices = list("Sunny"="sunny", "Overcast"="overcast", "Rainy"="rainy")),
                     sliderInput(inputId = "temp", label = "Temperature",min = 64, max = 86, value = 70),
                     sliderInput(inputId = "hum", label = "Humidity",min = 64, max = 96, value = 90),
                     selectInput(inputId = "windy", 
                                 label = "Windy",
                                 choices = list("Yes"="yes", "No"="no")),
                     actionButton(inputId = "submitbutton", label = "Submit", class='btn bnt-primary')
                   ),
                   
                   mainPanel(
                     tags$h3("Status/Output"),
                     verbatimTextOutput("contents"),
                     tableOutput("tabledata")
                   )
                 )
              ),
        tabPanel(title = "Vader Sentiment Analysis",
                 titlePanel("Data & Statistic Team"),
                 h3("Sentiment Analysis using VADER model"),
                 
                 # Sidebar with a slider input for number of bins 
                 sidebarLayout(
                   sidebarPanel(
                     textAreaInput("caption", "Enter your text to get it's Score after submitting:"),
                     actionButton("Vaderbutton", "Submit", class = "btn btn-primary")
                   ),
                   
                   # Show a plot of the generated distribution
                   mainPanel(
                     verbatimTextOutput("value")
                   )
                 )
                 ),
        tabPanel(title = "WB Indicators",
                 titlePanel("Data & Statistic Team"),
                 h3("Search Indicators in World Bank database"),
                 
                 # Sidebar with a slider input for number of bins 
                 sidebarLayout(
                   sidebarPanel(
                     textAreaInput("WBI", "What key words are you looking for?"),
                     actionButton("WBbutton", "Submit", class = "btn btn-primary")
                   ),
                   
                   # Show a plot of the generated distribution
                   mainPanel(
                     dataTableOutput("valueWBI")
                   )
                 )
                 ),
        tabPanel(title = "GHO Indicators",
                 titlePanel("Data & Statistic Team"),
                 h3("Search Indicators in Global Health Observatory database"),
                 
                 # Sidebar with a slider input for number of bins 
                 sidebarLayout(
                   sidebarPanel(
                     textAreaInput("GHOI", "What key words are you looking for?"),
                     actionButton("GHObutton", "Submit", class = "btn btn-primary")
                   ),
                   
                   # Show a plot of the generated distribution
                   mainPanel(
                     dataTableOutput("valueGHO")
                   )
                 )
        ),
        
        ),
    )

# Define server logic required to draw a histogram
server <- function(input, output) {
  
  # ------------------ App virtualenv setup (Do not edit) ------------------- #
  
  virtualenv_dir = Sys.getenv('VIRTUALENV_NAME')
  python_path = Sys.getenv('PYTHON_PATH')
  
  # Create virtual env and install dependencies
  reticulate::virtualenv_create(envname = virtualenv_dir, python = python_path)
  reticulate::virtualenv_install(virtualenv_dir, packages = PYTHON_DEPENDENCIES, ignore_installed=TRUE)
  reticulate::use_virtualenv(virtualenv_dir, required = T)
  
  reticulate::source_python("data/SearchIndicatorsWB.py")
  reticulate::source_python("data/SearchIndicatorsGHO.py")
  
  #Input Data
  datasetInput <- reactive({
    
    #Input data (outlook, temperature, humidity and windy) to data.frame for prediction
    df <- data.frame(
      Name = c('outlook', "temperature", "humidity", "windy"),
      Value = as.character(c(input$outlook, input$temp, input$hum, input$windy)),
      stringsAsFactors = FALSE
    )
    
    #play <- ''
    
    #df <- rbind(df, play)
    
    input <- transpose(df)
    
    write.table(input, "data/input.csv", sep = ",", quote = FALSE, row.names = FALSE, col.names = FALSE)
    
    test <- read.csv(paste("data/input", ".csv", sep = ""), header = TRUE)
    
    test$outlook <- factor(test$outlook, levels = c("overcast", "rainy", "sunny"))
    
    Output <- data.frame(Prediction = predict(model,test), round(predict(model,test,type = "prob"), 3))
    
    
  })
  
  
  
  #Status/Output Text Box
  output$contents <- renderText({
    if(input$submitbutton > 0){
      isolate("Calculation complete.")
    }else{
      return("Server is ready for calculation.")
    }
  })
  
  #Prediction results table
  output$tabledata <- renderTable({
    if(input$submitbutton > 0){
      isolate(datasetInput())
    }
  })
  
  sia <- reactive(get_vader(c(input$caption))[c("pos", "neu", "neg")])
  
  
  output$value <- renderPrint({ 
    if (input$Vaderbutton>0) { 
      isolate(sia()) 
    }
    
  })
  
  
  output$valueWBI <- DT::renderDataTable({
    if (input$WBbutton>0) {
      withProgress(message = 'Calculation in progress',
                   detail = 'This may take a while...', value = 0, {
                     return(SearchIndicatorsWB(input$WBI))
                   })
    }
    
  })
  
  output$valueGHO <- DT::renderDataTable({
    if (input$GHObutton>0) { 
      withProgress(message = 'Calculation in progress',
                   detail = 'This may take a while...', value = 0, {
                     return(SearchIndicatorsGHO(input$GHOI))
                   })
    }
    
  })
  
}

# Run the application 
shinyApp(ui = ui, server = server)
