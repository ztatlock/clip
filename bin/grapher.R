posts <- read.csv( 'posts.csv'
                 , colClasses = c( 'factor'    # city
                                 , 'factor'    # catg
                                 , 'character' # post
                                 , 'integer'   # year
                                 , 'integer'   # month
                                 , 'integer'   # day
                                 , 'integer'   # hour
                                 , 'integer'   # min
                                 , 'factor'    # ampm
                                 , 'factor'    # tzone
                                 , 'integer'   # tfhour
                                 , 'character' # t
                                 , 'character' # d
                                 , 'character' # dow
                                 ))

# massage some columns to nicer types
# use POSIXct since POSIXlt crashes aggregate!
posts$t <- as.POSIXct(strptime(posts$t, '%Y%m%d%H%M'))
posts$d <- as.POSIXct(strptime(posts$d, '%Y%m%d'))
posts$dow <- factor(posts$dow, ordered = TRUE,
               levels = c('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'))
summary(posts)

# date * dow * # posts
date.count <- with(posts,
                aggregate(post, FUN = length,
                  by = list(d=d, dow=dow)))
png('global-count.png')
plot(date.count$d, date.count$x)
dev.off()

# dow * avg # posts
dow.avg <- with(date.count,
             aggregate(x, FUN = mean,
               by = list(dow=dow)))
png('dow-avg.png')
barplot(dow.avg$x, names.arg = dow.avg$dow)
dev.off()

# date * city * # posts
png('cities-count.png')
for(cy in levels(posts$city)) {
  aux <- subset(posts, city == cy)
  aux <- with(aux,
           aggregate(post, FUN = length,
             by = list(d=d)))
  plot(aux$d, aux$x)
dev.off()

