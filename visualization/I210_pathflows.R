library(ggplot2)
require(reshape2)
size=10

data <- read.csv(file="../data/I210_attack/path_flows_routed.csv", header=TRUE)

long <- melt(data, id='ratio_routed')

g1 <- ggplot(long, aes(x=ratio_routed, y=value, colour=variable)) +
  #geom_point(size=3) + 
  geom_area(aes(colour=variable, fill=variable)) +
  xlab("percentage of navigation app users") +
  ylab("flow (veh/hour)") +
  ggtitle("Flow of routed users for each path") +
  theme(axis.text.x=element_text(size=size), 
        axis.title.x=element_text(size=size),
        axis.text.y=element_text(size=size), 
        axis.title.y=element_text(size=size),
        plot.title = element_text(size = size),
        legend.position="bottom",
        legend.text = element_text(size = size))
plot(g1)