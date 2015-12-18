##
## You should create one R script called run_analysis.R that does the following. 
##
## 1.   Merges the training and the test sets to create one data set.
## 2.   Extracts only the measurements on the mean and standard deviation for each measurement. 
## 3.   Uses descriptive activity names to name the activities in the data set
## 4.   Appropriately labels the data set with descriptive variable names. 
## 5.   From the data set in step 4, creates a second, 
##      independent tidy data set with the average of each variable for each activity and each subject.


#setwd("c://R//gacd//UCI HAR Dataset")
setwd("./UCI HAR Dataset")
#############
# TEST DATA #
#############
# Load X_test.txt
X_test = read.table(file = "test/X_test.txt" ,header = FALSE)
# Load y_test.txt
y_test = read.table(file = "test/y_test.txt" ,header = FALSE)
# Load subject_test.txt
subject_test = read.table(file = "test/subject_test.txt" ,header = FALSE)

# MERGE ALL TEST DATA
testall = cbind(subject_test,y_test,X_test)

#################
# TRAINING DATA #
#################
# Load X_train.txt
X_train = read.table(file = "train/X_train.txt" ,header = FALSE)
# Load y_test.txt
y_train = read.table(file = "train/y_train.txt" ,header = FALSE)
# Load subject_test.txt
subject_train = read.table(file = "train/subject_train.txt" ,header = FALSE)

# MERGE ALL TRAIN DATA
trainall = cbind(subject_train,y_train,X_train)

##################################
# 1. MERGE TRAINING AND DATA SET #
##################################
alldata = rbind(trainall,testall)

#Load data features
features = read.table("features.txt")

#AllData column names
colnames(alldata) <- c("Subject","Test Labels",as.character(features$V2))

#################################################################################################
## 2.   Extracts only the measurements on the mean and standard deviation for each measurement. #
#################################################################################################
# Subset columns with name that cointain "mean()" and "std()"

msdata <- alldata[,grep(c("Subject|Test Labels|mean()|std()"),colnames(alldata))]


####*############################################################################################
## 3.   Uses descriptive activity names to name the activities in the data set                  #
#################################################################################################

# Load activity_labels.txt
activity = read.table(file = "activity_labels.txt" ,header = FALSE)

#Set column names to match our data
colnames(activity) <- c("Test Labels", "Activity")

# Merge our data with activity labels
msdata_act = merge(msdata,activity,by.x="Test Labels", by.y="Test Labels",sort=TRUE)

#Drop Activity label colum
msdata_act[1] <- NULL


################################################################################################
## 4.   UAppropriately labels the data set with descriptive variable names.                    #
################################################################################################

#Done in step one

################################################################################################
##  5.From the data set in step 4, creates a second,                                           #
##      independent tidy data set with the average of each variable for each                   #
##           activity and each subject.                                                        #
################################################################################################


#Aggregate data by column Activity and Subject
msdata_clean <- aggregate(msdata_act, list(Activity=msdata_act$Activity,Subject=msdata_act$Subject),mean)

#Remove subject from source of aggregate
msdata_clean[,83] <- NULL
msdata_clean[,2] <- NULL

#Write data for upload
write.table(msdata_clean,"msdata_clean.txt" , row.name=FALSE)

