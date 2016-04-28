require(scales)

getwd()
#setwd("../data/LA")

data <- read.csv(file="total_link_flows.csv", header=TRUE)
n = nrow(data)
m = ncol(data)
data[,8:m] <- data[,8:m] * 4000.

highways <- data[data$local==0,]
local_roads <- data[data$local==1,]

# find index of the maximum flow, and the delta with the first and last
data[, "max"] <- apply(data[, 8:m], 1, max)
data[, "ind"] <- apply(data[, 8:m], 1, which.max)
data[, "inc"] <- 100.*(data$max - data$X0) / data$max
data[, "dec"] <- 100.*(data$max - data$X100) / data$max

#data <- data[data$max != 0.0,]
#data <- data[(data$inc > 5.) | (data$dec > 5.),]
#write.csv(data, file = "link_variation.csv", row.names=FALSE)

v <- as.data.frame(table(data$ind))

#for (i in 1:n) {
#  data[i,"index"] <- which.max(x)-8
#}

# local_roads <- local_roads[local_roads$X100>0.01,]

# plot
g1 <- ggplot(data[data$capacity<15000,], aes(capacity)) +
  geom_histogram(binwidth = 1000)
g1 <- ggplot(data[data$capacity<15000,], aes(x=capacity/1000.)) +
  geom_histogram(aes(y=..count../sum(..count..)), binwidth = 1) +
  scale_y_continuous(labels=percent) +
  xlab('road capacity (1000 veh/hour)') +
  theme(axis.title.y=element_blank(),
        axis.text.x=element_text(size=16),
        axis.title.x=element_text(size=16),
        axis.text.y=element_text(size=16))
plot(g1)
