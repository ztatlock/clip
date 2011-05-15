#!/usr/bin/env bash

ROOT=$1

function extract_links {
  cat $1 \
    | sed 's/href/\nhref/g' \
    | grep 'href' \
    | sed 's/^href=.//g' \
    | sed 's/.>.*$//g' \
    | grep '^http' \
    | sort \
    | uniq
}

function is_post {
  echo $1 \
    | egrep 'http://sandiego.craigslist.org/.../w4w/[0-9]*.html'
}

function extract_posts {
  links=$(extract_links root.html)
  for link in $links; do
    if is_post $link; then
      echo $link
    fi
  done
}

wget $ROOT -O root.html

for post in $(extract_posts root.html); do
  wget --force-directories $post
done
