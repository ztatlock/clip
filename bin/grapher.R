posts <- read.csv('posts.csv',
           colClasses = c( "factor"    # city
                         , "factor"    # catg
                         , "character" # post
                         , "integer"   # year
                         , "integer"   # month
                         , "integer"   # day
                         , "integer"   # hour
                         , "integer"   # min
                         , "factor"    # ampm
                         , "factor"    # tzone
                         , "integer"   # tfhour
                         , "character" # t
                         , "factor"    # dow
                         ))

