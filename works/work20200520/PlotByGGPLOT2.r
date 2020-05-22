
library(ggplot2)




df = read.csv("./tmp/data.csv")

p = ggplot(df, aes(x=time, y=value, color = varType))
p = p + geom_line()
p = p + facet_grid(weightOnError ~ epoch) 
p = p + xlab('Simulation steps')
p = p + ylab('')
ggsave('./tmp/response.png')
print(p)


df = read.csv("./tmp/gain.csv")

p = ggplot(df, aes(x = as.factor(epoch), y=value))
p = p + geom_boxplot()
p = p + facet_wrap(weightOnError ~ .)
p = p + xlab('Training iteration')
p = p + ylab('Gain')
ggsave('./tmp/gain.png')
print(p)
