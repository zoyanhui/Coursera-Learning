# Getting and Cleaning Data
# Course Project

### Install and load plyr package for step 5

if (!require("plyr")) {
  install.packages("plyr")
}

require("plyr")


### 1. Merges the training and the test sets to create one data set.

# read data into data.frames
subject_test <- read.table("./UCI HAR Dataset/test/subject_test.txt")
X_test <- read.table("./UCI HAR Dataset/test/X_test.txt")
y_test <- read.table("./UCI HAR Dataset/test/y_test.txt")

subject_train <- read.table("./UCI HAR Dataset/train/subject_train.txt")
X_train <- read.table("./UCI HAR Dataset/train/X_train.txt")
y_train <- read.table("./UCI HAR Dataset/train/y_train.txt")

# add column name for subject
colnames(subject_test) <- "subject"
colnames(subject_train) <- "subject"

# add column names for features
features <- read.table("./UCI HAR Dataset/features.txt")[, 2]
colnames(X_test) <- features
colnames(X_train) <- features

# add column name for activity
colnames(y_test) <- "activity"
colnames(y_train) <- "activity"

# combine files into one
test <- cbind(subject_test, y_test, X_test)
train <- cbind(subject_train, y_train, X_train)
combined <- rbind(train, test)


### 2. Extracts only the measurements on the mean and standard deviation for each measurement. 

# check columns contain "mean()" or "std()"
features_extract <- grepl("mean\\(\\)|std\\(\\)", features)
# for keeping subject and activity columns
features_extract <- c(TRUE, TRUE, features_extract)
# extract columns contain "mean()" or "std()" 
combined_extract <- combined[, features_extract] 


### 3. Uses descriptive activity names to name the activities in the data set

activity_labels <- read.table("./UCI HAR Dataset/activity_labels.txt")[, 2]
combined_extract$activity <- factor(combined_extract$activity, labels=activity_labels)


### 4. Appropriately labels the data set with descriptive variable names. 

# t -> time, f -> frequency
# Acc -> Accelerometer, Gyro -> Gyroscope
# Mag -> Magnitude, BodyBody -> Body
colnames(combined_extract)<-gsub("^t", "time", colnames(combined_extract))
colnames(combined_extract)<-gsub("^f", "frequency", colnames(combined_extract))
colnames(combined_extract)<-gsub("Acc", "Accelerometer", colnames(combined_extract))
colnames(combined_extract)<-gsub("Gyro", "Gyroscope", colnames(combined_extract))
colnames(combined_extract)<-gsub("Mag", "Magnitude", colnames(combined_extract))
colnames(combined_extract)<-gsub("BodyBody", "Body", colnames(combined_extract))


### 5. From the data set in step 4, creates a second, independent tidy data set with the average of 
### each variable for each activity and each subject.

data <- aggregate(. ~subject + activity, combined_extract, mean)
data <- data[order(data$subject, data$activity), ]
write.table(data, file = "tidydata.txt", row.names = FALSE)
