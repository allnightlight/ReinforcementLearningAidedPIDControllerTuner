
library(ggplot2)


dfOrg = read.csv("./param_casestudy5c.csv")

timeSimulationToPlot = c(255, 4351, 8191, 12543, 16383)

df = dfOrg[dfOrg$timeSimulation %in% timeSimulationToPlot,]
df = df[df$gain>-3,]
df = df[df$fixPolicySd=="fixPolicySd = 0",]

p = ggplot(df, aes(x = as.factor(timeSimulation), y=gain, group=buildOrderId))
p = p + geom_line(size=1, color="gray")
p = p + geom_point(size=1, color="black", shape = 16)
#p = p + facet_grid(. ~  fixPolicySd + fixPolicyScale)
p = p + facet_wrap(fixPolicyScale ~  .)
p = p + xlab('Training iteration')
p = p + ylab('Gain')
ggsave('./tmp/p_gain_training_process_casestudy005c.png', width = 7, height = 7)
print(p)


p = ggplot(df, aes(x = as.factor(timeSimulation), y=gain))
p = p + geom_boxplot()
#p = p + facet_grid(fixPolicyScale ~ fixPolicySd)
p = p + facet_wrap(fixPolicyScale ~ .)
#p = p + facet_grid(. ~  fixPolicySd + fixPolicyScale)
p = p + xlab('Training iteration')
p = p + ylab('Gain')
ggsave('./tmp/p_gain_distribution_casestudy005c.png', width = 7, height = 7)
print(p)

p = ggplot(df, aes(x = as.factor(timeSimulation), y=sd, group=buildOrderId))
p = p + geom_line(size=1, color="gray")
p = p + geom_point(size=1, color="black", shape = 16)
#p = p + facet_grid(fixPolicyScale ~ fixPolicySd)
p = p + facet_wrap(fixPolicyScale ~ .)
#p = p + facet_grid(. ~  fixPolicySd + fixPolicyScale)
p = p + xlab('Training iteration')
p = p + ylab('Standard Deviation of Policy Prob.')
p = p + scale_y_log10()
ggsave('./tmp/policy_sd_training_process_casestudy005c.png', width = 7, height = 7)
print(p)

p = ggplot(df, aes(x = as.factor(timeSimulation), y=sd))
p = p + geom_boxplot()
#p = p + facet_grid(fixPolicyScale ~ fixPolicySd)
p = p + facet_wrap(fixPolicyScale ~ .)
#p = p + facet_grid(. ~  fixPolicySd + fixPolicyScale)
p = p + xlab('Training iteration')
p = p + ylab('Standard Deviation of Policy Prob.')
p = p + scale_y_log10()
ggsave('./tmp/policy_sd_distribution_casestudy005c.png', width = 7, height = 7)
print(p)


df = dfOrg[dfOrg$timeSimulation %in% timeSimulationToPlot,]
df = df[df$fixPolicySd=="fixPolicySd = 0",]

p = ggplot(df, aes(x = as.factor(timeSimulation), y=gain, group=buildOrderId))
p = p + geom_line(size=1, color="gray")
p = p + geom_point(size=1, color="black", shape = 16)
#p = p + facet_grid(. ~  fixPolicySd + fixPolicyScale)
p = p + facet_wrap(fixPolicyScale ~  .)
p = p + xlab('Training iteration')
p = p + ylab('Gain')
ggsave('./tmp/p_gain_training_process_casestudy005c_with_outliers.png', width = 7, height = 7)
print(p)

