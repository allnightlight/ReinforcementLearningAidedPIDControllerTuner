
library(ggplot2)

df = read.csv("data.csv")

p = ggplot(df, aes(x=time, y=value, color = varType))
p = p + geom_line()
p = p + facet_grid(weightOnError~epoch)
p = p + xlab('Simulation steps')
p = p + ylab('')
ggsave('response.png')
print(p)

