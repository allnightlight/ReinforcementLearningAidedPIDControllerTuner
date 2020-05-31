
library(ggplot2)


df = read.csv("./param_casestudy4.csv")

timeSimulationToPlot = c(255, 2815, 5375, 8191)

df = df[df$timeSimulation %in% timeSimulationToPlot,]

p = ggplot(df, aes(x = as.factor(timeSimulation), y=gain, group=buildOrderId))
p = p + geom_line(size=1, color="gray")
p = p + geom_point(size=1, color="black", shape = 16)
p = p + facet_wrap(weightOnError ~ .)
p = p + xlab('Training iteration')
p = p + ylab('Gain')
ggsave('./tmp/p_gain_training_process.png')
print(p)


p = ggplot(df, aes(x = as.factor(timeSimulation), y=gain))
p = p + geom_boxplot()
p = p + facet_wrap(weightOnError ~ .)
p = p + xlab('Training iteration')
p = p + ylab('Gain')
ggsave('./tmp/p_gain_distribution.png')
print(p)

p = ggplot(df, aes(x = as.factor(timeSimulation), y=sd, group=buildOrderId))
p = p + geom_line(size=1, color="gray")
p = p + geom_point(size=1, color="black", shape = 16)
p = p + facet_wrap(weightOnError ~ .)
p = p + xlab('Training iteration')
p = p + ylab('Standard Deviation of Policy Prob.')
p = p + scale_y_log10()
ggsave('./tmp/p_sd_training_process.png')
print(p)
