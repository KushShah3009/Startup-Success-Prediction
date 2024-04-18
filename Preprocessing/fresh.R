objects <- read.csv("objects.csv")
objectsDF <- objects
objectsDF <- objectsDF[,c("entity_type","entity_id","category_code","status","founded_at","closed_at","country_code","first_investment_at",
                          "last_investment_at","investment_rounds","invested_companies",
                          "first_funding_at","last_funding_at","funding_rounds",
                          "funding_total_usd","first_milestone_at","last_milestone_at",
                          "milestones","relationships")]

library("dplyr")
library("tidyverse")
objectsDF <- filter(objectsDF, objectsDF$category_code !="")
objectsDF <- filter(objectsDF, objectsDF$founded_at !="")
objectsDF <- filter(objectsDF, objectsDF$country_code !="")
objectsDF <- filter(objectsDF, objectsDF$entity_id != 75959 ) #ONE COMAPNY 75959 HAS FOUNDATION DATE = FIRST INVESTMENT = LAST INVESTMENT IT SEEMS FAULTY SO REMOVING IT
objectsDF <- filter(objectsDF, objectsDF$entity_id != 193342)
objectsDF <- filter(objectsDF, objectsDF$entity_id != 42709) # no iverstment data


country <- objectsDF %>% 
  group_by(country_code) %>% 
  summarise(N = n())

country$countryfreq <- country$N / sum(country$N)
country <- select(country, c("country_code","countryfreq"))
objectsDF <- merge(objectsDF,country,by="country_code")


category <- objectsDF %>% 
  group_by(category_code) %>% 
  summarise(N = n())

category$categoryfreq <- category$N / sum(category$N)
category <- select(category, c("category_code","categoryfreq"))
objectsDF <- merge(objectsDF,category,by="category_code")



objectsDF$closed_at <- ifelse(objectsDF$closed_at=="", NA, objectsDF$closed_at)
objectsDF$first_investment_at <- ifelse(objectsDF$first_investment_at=="", NA, objectsDF$first_investment_at)
objectsDF$last_investment_at <- ifelse(objectsDF$last_investment_at=="", NA, objectsDF$last_investment_at)
objectsDF$first_funding_at <- ifelse(objectsDF$first_funding_at=="", NA, objectsDF$first_funding_at)
objectsDF$last_funding_at <- ifelse(objectsDF$last_funding_at=="",NA,objectsDF$last_funding_at)
objectsDF$first_milestone_at <- ifelse(objectsDF$first_milestone_at=="", NA, objectsDF$first_milestone_at)
objectsDF$last_milestone_at <- ifelse(objectsDF$last_milestone_at=="", NA,objectsDF$last_milestone_at)


objectsDF$founded_at <- as.POSIXct(objectsDF$founded_at, format="%Y-%m-%d")
objectsDF$closed_at <- as.POSIXct(objectsDF$closed_at, format="%Y-%m-%d")
objectsDF$first_investment_at <- as.POSIXct(objectsDF$first_investment_at, format="%Y-%m-%d")
objectsDF$last_investment_at <- as.POSIXct(objectsDF$last_investment_at, format="%Y-%m-%d")
objectsDF$first_funding_at <- as.POSIXct(objectsDF$first_funding_at, format="%Y-%m-%d")
objectsDF$last_funding_at <- as.POSIXct(objectsDF$last_funding_at, format="%Y-%m-%d")
objectsDF$first_milestone_at <- as.POSIXct(objectsDF$first_milestone_at, format="%Y-%m-%d")
objectsDF$last_milestone_at <- as.POSIXct(objectsDF$last_milestone_at, format="%Y-%m-%d")
objectsDF <- drop_na(objectsDF,c("founded_at"))

objectsDF$timeininvestment <- case_when(
  objectsDF$investment_rounds != 0 ~  abs(as.numeric(difftime(objectsDF$last_investment_at,objectsDF$founded_at,units = "days"))),
  objectsDF$investment_rounds == 0 ~ -1
)

objectsDF$investmentaffinity <- (objectsDF$invested_companies * objectsDF$investment_rounds) / exp(objectsDF$timeininvestment)

objectsDF$timeinfunding <- case_when(
  objectsDF$funding_rounds != 0  ~abs(as.numeric(difftime(objectsDF$last_funding_at,objectsDF$founded_at,units = "days"))),
  objectsDF$funding_rounds == 0 ~ -1
)

objectsDF <- drop_na(objectsDF,c("timeinfunding")) #no funding data
objectsDF$fundingaffinity <- (objectsDF$funding_total_usd* objectsDF$funding_rounds) / exp(objectsDF$timeinfunding)

objectsDF$timeinmilestone <- case_when(
  objectsDF$milestones == 0 ~ -1,
  objectsDF$milestones != 0 ~ abs(as.numeric(difftime(objectsDF$last_milestone_at,objectsDF$founded_at, units = "days")))
)

objectsDF$outcome <- case_when(
  objectsDF$status == "closed" | objectsDF$status == "operating" ~ 0,
  objectsDF$status == "ipo" | objectsDF$status == "acquired" ~ 1
)

mlmodel <- objectsDF[,c("countryfreq", "categoryfreq","investmentaffinity","fundingaffinity","milestones","timeinmilestone","relationships","outcome")]
#write.csv(mlmodel,"finaldata.csv")
