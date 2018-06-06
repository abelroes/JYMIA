library(readr)

#Lê CSV original
adult2 <- read.table("http://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data",
                sep=",",header=F,col.names=c("age", "type.employer", "fnlwgt", "education", 
                                               "education.num","marital", "occupation", "relationship", "race","sex",
                                               "capital.gain", "capital.loss", "hours.per.week","country", "income"),
                  fill=FALSE,strip.white=T)
#Grava CSV para ser tratado
write.csv(adult2, file = "../JYMIA/adult2.csv", row.names = FALSE)
#Retira colunas desnecessárias
adult2[["education.num"]]=NULL
adult2[["fnlwgt"]]=NULL

#Sanitização dos Dados
adult2 <- subset(adult2, adult2$age != "?")
adult2 <- subset(adult2, adult2$type.employer != "?")
adult2 <- subset(adult2, adult2$education != "?")
adult2 <- subset(adult2, adult2$marital != "?")
adult2 <- subset(adult2, adult2$occupation != "?")
adult2 <- subset(adult2, adult2$relationship != "?")
adult2 <- subset(adult2, adult2$race != "?")
adult2 <- subset(adult2, adult2$sex != "?")
adult2 <- subset(adult2, adult2$capital.gain != "?")
adult2 <- subset(adult2, adult2$capital.loss != "?")
adult2 <- subset(adult2, adult2$hours.per.week != "?")
adult2 <- subset(adult2, adult2$country != "?")
adult2 <- subset(adult2, adult2$income != "?")

write.csv(adult2, file = "../JYMIA/adult2.csv", row.names = FALSE)


#Discretização age
varDiv <- (max(adult2$age) - min(adult2$age))/5
adult2$cat.age[adult2$age >= 15 & adult2$age < 30] = "15-30"
adult2$cat.age[adult2$age >= 30 & adult2$age < 45] = "30-45"
adult2$cat.age[adult2$age >= 45 & adult2$age < 60] = "45-60"
adult2$cat.age[adult2$age >= 60 & adult2$age < 75] = "60-75"
adult2$cat.age[adult2$age >= 75 & adult2$age <= 90] = "75-90"
table(adult2$cat.age)

#Discretização capital-gain
varDiv <- ceiling((max(adult2$capital.gain) - min(adult2$capital.gain))/5)
adult2$cat.capital.gain[adult2$capital.gain >= 0 & adult2$capital.gain < varDiv] = "Very Low"
adult2$cat.capital.gain[adult2$capital.gain >= varDiv & adult2$capital.gain < (varDiv*2)] = "Low"
adult2$cat.capital.gain[adult2$capital.gain >= (varDiv*2) & adult2$capital.gain < (varDiv*3)] = "Medium"
adult2$cat.capital.gain[adult2$capital.gain >= (varDiv*3) & adult2$capital.gain < (varDiv*4)] = "High"
adult2$cat.capital.gain[adult2$capital.gain >= (varDiv*4) & adult2$capital.gain <= (varDiv*5)] = "Very High"
table(adult2$cat.capital.gain)

#Discretização capital-loss
varDiv <- ceiling((max(adult2$capital.loss) - min(adult2$capital.loss))/5)
adult2$cat.capital.loss[adult2$capital.loss >= 0 & adult2$capital.loss < varDiv] = "Very Low"
adult2$cat.capital.loss[adult2$capital.loss >= varDiv & adult2$capital.loss < (varDiv*2)] = "Low"
adult2$cat.capital.loss[adult2$capital.loss >= (varDiv*2) & adult2$capital.loss < (varDiv*3)] = "Medium"
adult2$cat.capital.loss[adult2$capital.loss >= (varDiv*3) & adult2$capital.loss < (varDiv*4)] = "High"
adult2$cat.capital.loss[adult2$capital.loss >= (varDiv*4) & adult2$capital.loss <= (varDiv*5)] = "Very High"
table(adult2$cat.capital.loss)

#Discretização hours-per-week
varDiv <- ceiling((max(adult2$hours.per.week) - min(adult2$hours.per.week))/5)
adult2$cat.hours.per.week[adult2$hours.per.week >= 0 & adult2$hours.per.week < varDiv] = "Very Low"
adult2$cat.hours.per.week[adult2$hours.per.week >= varDiv & adult2$hours.per.week < (varDiv*2)] = "Low"
adult2$cat.hours.per.week[adult2$hours.per.week >= (varDiv*2) & adult2$hours.per.week < (varDiv*3)] = "Medium"
adult2$cat.hours.per.week[adult2$hours.per.week >= (varDiv*3) & adult2$hours.per.week < (varDiv*4)] = "High"
adult2$cat.hours.per.week[adult2$hours.per.week >= (varDiv*4) & adult2$hours.per.week <= (varDiv*5)] = "Very High"
table(adult2$cat.hours.per.week)

#Descarta colunas não categóricas
names(adult2)
adult2[["age"]]=NULL
adult2[["capital.gain"]]=NULL
adult2[["capital.loss"]]=NULL
adult2[["hours.per.week"]]=NULL

#Reordena colunas
adult2 <- adult2[, c(10, 1:8, 11:13, 9)]
names(adult2)
#Grava arquivo final
write.csv(adult2, file = "../JYMIA/adult2.csv", row.names = FALSE)

#FIM
