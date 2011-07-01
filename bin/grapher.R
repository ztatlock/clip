posts <- read.csv('posts.csv',
           colClasses = c( "factor"    # city
                         , "factor"    # catg
                         , "character" # post
                         , "integer"   # year
                         , "integer"   # month
                         , "integer"   # day
                         , "integer"   # hour
                         , "integer"   # minute
                         , "factor"    # ampm
                         , "factor"    # tzone
                         , "integer"   # tfhour
                         , "factor"    # dow
                         ))

