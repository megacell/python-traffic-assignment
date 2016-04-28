library(ggplot2)
require(reshape2)
source('multiplot.R')

getwd()
#setwd("python-traffic-assignment/visualization")
#setwd("../../visualization")

#data <- read.csv(file="../data/I210/out.csv", header=TRUE)
#data <- read.csv(file="../data/chicago/out.csv", header=TRUE)
#data <- read.csv(file="../data/LA/copy/out.csv", header=TRUE)
#data <- read.csv(file="../data/I210_modified/out.csv", header=TRUE)
#data <- read.csv(file="../data/LA/copy_2/out.csv", header=TRUE)
data <- read.csv(file="../data/LA/out.csv", header=TRUE)

data$flow <- data$flow / 1000000.
data$flow_local <- data$flow_local / 1000000.
data$flow_non_local <- data$flow_non_local / 1000000.

data$ratio_routed <- data$ratio_routed * 100.
long <- melt(data, id='ratio_routed')
size = 16
xlabel <- "percentage of navigation app users"

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
g9 <- ggplot(long[long$variable %in% c('flow_non_local', 'flow_local'),], aes(x=ratio_routed, y=value, colour=variable)) +
  #geom_point(size=3) + 
  geom_area(aes(colour=variable, fill=variable)) +
  xlab(xlabel) +
  ylab("flow (M veh/hour)") +
  ggtitle("Total flow") +
  scale_fill_manual(name="", values=c('red', 'blue'), labels=c("on local roads", "on non-local roads")) +
  scale_color_manual(name="", values=c('red', 'blue'), labels=c("on local roads", "on non-local roads")) +
  theme(axis.text.x=element_text(size=size), 
        axis.title.x=element_text(size=size),
        axis.text.y=element_text(size=size), 
        axis.title.y=element_text(size=size),
        plot.title = element_text(size = size))


plot(g9)#g1 g2 g3
#multiplot(g4,g5)
#multiplot(g6,g7)