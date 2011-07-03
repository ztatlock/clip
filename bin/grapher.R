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

# massage some columns to get nicer types
posts$t <- strptime(posts$t, '%Y%m%d%H%M')
posts$d <- strptime(posts$d, '%Y%m%d')
posts$dow <- factor( posts$dow
                   , levels = c('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
                   , ordered = TRUE
                   )
summary(posts)

x <- with(posts, aggregate( post
                          , by = list(d=d)
                          , FUN = length
                          ))
summary(x)

x <- with(posts, aggregate( post
                          , by = list(dow=dow)
                          , FUN = length
                          ))
summary(x)

