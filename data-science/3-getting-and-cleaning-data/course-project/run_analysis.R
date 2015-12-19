if(!require("data.table")){
    install.packages("data.table")
    require("data.table")
}
if (!require("reshape2")) {
  install.packages("reshape2")
  require("reshape2")
}

# 0. Load data from csv file
## Load data features
features <- read.table("./UCI HAR Dataset/features.txt")

# Load activity labels
activity_labels <- read.table("./UCI HAR Dataset/activity_labels.txt")

# Load train subjects
train_subjects <- read.table("./UCI HAR Dataset/train/subject_train.txt")
colnames(train_subjects) <- "subject"

# Load train data
train_x <- read.table("./UCI HAR Dataset/train/X_train.txt")
train_y <- read.table("./UCI HAR Dataset/train/y_train.txt")

# Load test subjects
test_subjects <- read.table("./UCI HAR Dataset/test/subject_test.txt")
colnames(test_subjects) <- "subject"

# Load test data
test_x <- read.table("./UCI HAR Dataset/test/X_test.txt")
test_y <- read.table("./UCI HAR Dataset/test/y_test.txt")


# 1. Merges the training and the test sets to create one data set.
## Apply feature names to X, both train_x and test_x
features <- features[,2]
colnames(train_x) <- features
colnames(test_x) <- features

## Apply activity name to Y, both train and test data
colnames(train_y) <- "activity"
colnames(test_y) <- "activity"

## Combine x, y and subject
train_data <-cbind(train_subjects, train_y, train_x)
test_data <- cbind(test_subjects, test_y, test_x)

## Combine train and test data
all_data <- rbind(train_data, test_data)


# 2. Extracts only the measurements on the mean and standard deviation for each measurement. 
extract_features <- features[grepl("mean|std", features)]
all_data <- all_data[, c("subject", "activity", as.vector(extract_features))]

# 3. Uses descriptive activity names to name the activities in the data set
colnames(activity_labels) <- c("activity", "activity_name")
all_data$activity <- activity_labels[all_data$activity,"activity_name"]

# 4. Appropriately labels the data set with descriptive variable names. 
## This step done before

# 5. From the data set in step 4, creates a second, independent
#    tidy data set with the average of each variable for each 
#    activity and each subject.
melt_data <- melt(all_data, id=c("subject","activity"), variable.name = 'feature')
tidy_data <- dcast(melt_data, subject + activity ~ feature, mean)

## 6. Write tidy data to file
write.table(tidy_data, file = "./tidy_data.txt", row.name=FALSE)

