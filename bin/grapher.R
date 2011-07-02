
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
                                 , 'character' # dow
                                 )
                 )

posts$t <- strptime(posts$t, '%Y%m%d%H%M')

posts$dow <- factor( posts$dow
                   , levels = c('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
                   , ordered = TRUE
                   )

summary(posts)
