
library(ggplot2)
require(reshape2)
source('multiplot.R')

#<<<<<<< Updated upstream
#getwd()
#setwd("python-traffic-assignment/visualization")
#setwd("../../visualization")
#=======
#setwd("Documents/python-traffic-assignment/visualization")
# source("graphs.R", print.eval=TRUE)
# source("I210_pathflows.R", print.eval=TRUE)
#>>>>>>> Stashed changes

data <- read.csv(file="../data/I210/out.csv", header=TRUE)
#data <- read.csv(file="../data/chicago/out.csv", header=TRUE)
#data <- read.csv(file="../data/LA/copy/out.csv", header=TRUE)
#data <- read.csv(file="../data/I210_modified/out.csv", header=TRUE)
#data <- read.csv(file="../data/LA/copy_2/out.csv", header=TRUE)
#data <- read.csv(file="../data/LA/out.csv", header=TRUE)

data$vmt <- data$vmt / 1000000.
data$vmt_local <- data$vmt_local / 1000000.
data$vmt_non_local <- data$vmt_non_local / 1000000.

data$ratio_routed <- data$ratio_routed * 100.
long <- melt(data, id='ratio_routed')
size = 16
xlabel <- "percentage of routed users"

# average travel times for routed and non-routed
g1 <- ggplot(long[long$variable %in% c('tt_non_routed', 'tt_routed'),], aes(x=ratio_routed, y=value, colour=variable)) + 
  #geom_point(size=3) + 
  geom_line(size=1) + 
  xlab(xlabel) +
  ylab("time (min)") +
  ggtitle("Average travel time") +
  scale_colour_discrete(name="", labels=c("without navigation", "with navigation")) +
  theme(axis.text.x=element_text(size=size), 
        axis.title.x=element_text(size=size),
        axis.text.y=element_text(size=size), 
        axis.title.y=element_text(size=size),
        legend.position="bottom",
        legend.text = element_text(size = size))
  

# average travel times 
g2 <- ggplot(long[long$variable %in% c('tt_non_local', 'tt_local'),], aes(x=ratio_routed, y=value, colour=variable)) +
  #geom_point(size=3) + 
  geom_area(aes(colour=variable, fill=variable)) +
  xlab(xlabel) +
  ylab("time (min)") +
  ggtitle("Average travel time for one vehicle ") +
  scale_fill_manual(name="", values=c('red', 'blue'), labels=c("on local roads", "on non-local roads")) +
  scale_color_manual(name="", values=c('red', 'blue'), labels=c("on local roads", "on non-local roads")) +
  theme(axis.text.x=element_text(size=size), 
        axis.title.x=element_text(size=size),
        axis.text.y=element_text(size=size), 
        axis.title.y=element_text(size=size),
        plot.title = element_text(size = size))


# gas emissions
g3 <- ggplot(long[long$variable %in% c('gas_non_local', 'gas_local'),], aes(x=ratio_routed, y=value, colour=variable)) +
  #geom_point(size=3) + 
  geom_area(aes(colour=variable, fill=variable)) +
  xlab(xlabel) +
  ylab("emissions (gram/mile)") +
  ggtitle("Average CO2 emissions for one vehicle ") +
  scale_fill_manual(name="", values=c('red', 'blue'), labels=c("on local roads", "on non-local roads")) +
  scale_color_manual(name="", values=c('red', 'blue'), labels=c("on local roads", "on non-local roads")) +
  theme(axis.text.x=element_text(size=size), 
        axis.title.x=element_text(size=size),
        axis.text.y=element_text(size=size), 
        axis.title.y=element_text(size=size),
        plot.title = element_text(size = size))

# average total travel time
g4 <- ggplot(long[long$variable=='tt',], aes(x=ratio_routed, y=value, colour=variable)) + 
  #geom_point(size=3) + 
  geom_line(size=1) + 
  xlab(xlabel) +
  ylab("time (min)") +
  ggtitle("Average travel time for one vehicle ") +
  scale_color_manual(name="", values=c('blue')) +
  theme(axis.text.x=element_text(size=size), 
        axis.title.x=element_blank(),
        axis.text.y=element_text(size=size), 
        axis.title.y=element_text(size=size),
        legend.position="none")


# average total travel time
g5 <- ggplot(long[long$variable=='tt_local',], aes(x=ratio_routed, y=value, colour=variable)) + 
  #geom_point(size=3) + 
  geom_line(size=1) + 
  xlab(xlabel) +
  ylab("time (min)") +
  ggtitle("Average time spent on local roads for one vehicle ") +
  scale_color_manual(name="", values=c('red')) +
  theme(axis.text.x=element_text(size=size), 
        axis.title.x=element_text(size=size),
        axis.text.y=element_text(size=size), 
        axis.title.y=element_text(size=size),
        legend.position="none")

# average total travel time
g6 <- ggplot(long[long$variable=='gas',], aes(x=ratio_routed, y=value, colour=variable)) + 
  #geom_point(size=3) + 
  geom_line(size=1) + 
  xlab(xlabel) +
  ylab("emissions (gram/mile)") +
  ggtitle("Average CO2 emissions for one vehicle ") +
  scale_color_manual(name="", values=c('blue')) +
  theme(axis.text.x=element_text(size=size), 
        axis.title.x=element_blank(),
        axis.text.y=element_text(size=size), 
        axis.title.y=element_text(size=size),
        legend.position="none")


# average total travel time
g7 <- ggplot(long[long$variable=='gas_local',], aes(x=ratio_routed, y=value, colour=variable)) + 
  #geom_point(size=3) + 
  geom_line(size=1) + 
  xlab(xlabel) +
  ylab("emissions (gram/mile)") +
  ggtitle("Average CO2 emissions on local roads for one vehicle ") +
  scale_color_manual(name="", values=c('red')) +
  theme(axis.text.x=element_text(size=size), 
        axis.title.x=element_text(size=size),
        axis.text.y=element_text(size=size), 
        axis.title.y=element_text(size=size),
        legend.position="none")

g8 <- ggplot(long[long$variable %in% c('tt_non_routed', 'tt_routed'),], aes(x=ratio_routed, y=value, colour=variable)) + 
  #geom_point(size=3) + 
  theme(panel.grid.minor =   element_line(size=1),
        panel.grid.major =   element_line(size=1.5)) +
  geom_line(size=2) + 
  xlab(xlabel) +
  ylab("time (min)") +
  scale_colour_discrete(name="", labels=c("without navigation", "with navigation")) +
  theme(axis.text.x=element_blank(), 
        axis.title.x=element_blank(),
        axis.text.y=element_blank(), 
        axis.title.y=element_blank(),
        legend.position="none",
        legend.text = element_blank())

# total flow 
g9 <- ggplot(long[long$variable %in% c('vmt_non_local', 'vmt_local'),], aes(x=ratio_routed, y=value, colour=variable)) +
  #geom_point(size=3) + 
  geom_area(aes(colour=variable, fill=variable)) +
  xlab(xlabel) +
  ylab("VMT (million miles / hour)") +
  scale_fill_manual(name="", values=c('red', 'blue'), labels=c("on local roads", "on non-local roads")) +
  scale_color_manual(name="", values=c('red', 'blue'), labels=c("on local roads", "on non-local roads")) +
  theme(axis.text.x=element_text(size=size), 
        axis.title.x=element_text(size=size),
        axis.text.y=element_text(size=size), 
        axis.title.y=element_text(size=size),
        plot.title = element_text(size = size),
        legend.position="top",
        legend.title=element_text(size=size),
        legend.text=element_text(size=size))

# total VMT in the network
g10 <- ggplot(data, aes(x=ratio_routed, y=vmt, colour='red')) + 
  scale_color_manual(values=c("blue")) +
  #geom_point(size=3) + 
  geom_line(size=1) + 
  xlab(xlabel) +
  ylab("VMT (M miles/hour)") +
  theme(axis.text.x=element_text(size=size), 
        axis.title.x=element_text(size=size),
        axis.text.y=element_text(size=size), 
        axis.title.y=element_text(size=size),
        legend.position="none",
        legend.text = element_text(size = size))

g11 <- ggplot(data, aes(x=ratio_routed, y=vmt_local, colour='blue')) + 
  scale_color_manual(values=c("red")) +
  #geom_point(size=3) + 
  geom_line(size=1) + 
  xlab(xlabel) +
  ylab("VMT (M miles/hour)") +
  theme(axis.text.x=element_text(size=size), 
        axis.title.x=element_text(size=size),
        axis.text.y=element_text(size=size), 
        axis.title.y=element_text(size=size),
        legend.position="none",
        legend.text = element_text(size = size))

<<<<<<< Updated upstream
# compute marginal costs

delta <- data.frame(matrix(ncol = 6, nrow = 11))
colnames(delta) <- c('ratio_routed', 'd_vmt','d_vmt_local','zero','r_vmt','r_vmt_local')
delta[,1] <- data$ratio_routed
delta[,4] <- 0.
delta[1,2] <- 1000. * 0.1 * (data[2,]$vmt - data[1,]$vmt)
delta[1,3] <- 1000. * 0.1 * (data[2,]$vmt_local - data[1,]$vmt_local)
delta[11,2] <- 1000. * 0.1 * (data[11,]$vmt - data[10,]$vmt)
delta[11,3] <- 1000. * 0.1 * (data[11,]$vmt_local - data[10,]$vmt_local)
for (i in 2:10) {
  delta[i,2] <- 1000. * .05 * (data[i+1,]$vmt - data[i-1,]$vmt)
  delta[i,3] <- 1000. * .05 * (data[i+1,]$vmt_local - data[i-1,]$vmt_local)
  delta[i,5] <- 100.*(data[i+1,]$vmt - data[i,]$vmt) / data[i,]$vmt
  delta[i,6] <- 100.*(data[i+1,]$vmt_local - data[i,]$vmt_local) / data[i,]$vmt_local
}

long_d <- melt(delta[,1:4], id="ratio_routed")

# marginal cost of VMT in the network
g12 <- ggplot(long_d, aes(x=ratio_routed, y=value, colour=variable, linetype=variable)) + 
  scale_color_manual(values=c("blue", "red", "black"), labels=c("global", "low-cap", "x=0")) +
  scale_linetype_manual(values=c("solid", "solid", "dotted")) +
  #geom_point(size=3) + 
  geom_line(size=1) + 
  xlab(xlabel) +
  ylab("VMT (1K/hour/percent)") +
  ylim(-15,15) +
  theme(axis.text.x=element_text(size=1.5*size), 
        axis.title.x=element_text(size=1.5*size),
        axis.text.y=element_text(size=1.5*size), 
        axis.title.y=element_text(size=1.5*size),
        legend.position="top",
        legend.text = element_text(size = 1.5*size))

# relative variation in VMT
long_r <- melt(delta[2:10,c(1,5,6)], id="ratio_routed")
long_r_1 <- long_r[long_r$variable=='r_vmt',]
long_r_2 <- long_r[long_r$variable=='r_vmt_local',]
g14 <- ggplot() + geom_bar(data=long_r_1, aes(x=ratio_routed, y=value, fill=variable), stat="identity") +
  geom_bar(data=long_r_2, aes(x=ratio_routed, y=value, fill=variable), stat="identity") +
  ylab("relative variation") +
  scale_fill_manual(name="", values=c("blue","red"), labels=c("global", "low-cap")) +
  scale_x_discrete("percentage of routed users", 
                   breaks = c("10","20","30","40","50","60","70","80","90")) +
  theme(axis.text.x=element_text(size=1.5*size), 
        axis.title.x=element_text(size=1.5*size),
        axis.text.y=element_text(size=1.5*size), 
        axis.title.y=element_text(size=1.5*size),
        legend.position="top",
        legend.text = element_text(size = 1.5*size))

plot(g14)#g1 g2 g3, g9, g12, g14
=======
plot(g3)#g1 g2 g3
>>>>>>> Stashed changes
#multiplot(g4,g5)
#multiplot(g6,g7)
#multiplot(g10,g11)
