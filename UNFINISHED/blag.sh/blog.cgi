#!/bin/sh

BLOGDIR="./.blog"
TITLE="Kurt H. Maier INTERNET"

COMMAND=`echo "$QUERY_STRING" | sed -e 's/^.*?\(.*\).*/\1/; s/=.*//'`
LATEST_POST=`ls -t $BLOGDIR | head -1`
KWORD_TARGET=`echo "$QUERY_STRING" | sed -n 's/^.*keyword=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
SHOW_TARGET=`echo "$QUERY_STRING" | sed -n 's/^.*show=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
RSS_TARGET=`echo "$QUERY_STRING" | sed -n 's/^.*rss=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`

function starthtml {
  echo "Content-type: text/html; charset=utf-8"
  echo ""
  echo "<?xml version='1.0' encoding='UTF-8'?> <!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.1//EN' 'http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd'>"
      
#  echo "<!DOCTYPE html PUBLIC '-//W3C//DTD HTML 4.01//EN' 'http://www.w3.org/TR/html4/strict.dtd'>"
  echo "<html  xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' ><head> <title>$TITLE</title> <link rel='stylesheet' type='text/css' href='/blog.css' />"
  echo "<link rel='alternate' type='application/rss+xml' title='RSS 2.0' href='http://$SERVER_NAME$SCRIPT_NAME?rss=' /> </head><body>"
  echo "<div class='titlebar'><h1><a href='http://$SERVER_NAME$SCRIPT_NAME'>Kurt H. Maier</a></h1><h2>a largely pointless personal website</h2></div>"
  echo "<div class='container'>"
}

function keywordsearch {
  
  echo "<h3>Posts matching \"$KWORD_TARGET\"</h3> <ul>"
  for i in $MATCHING_POSTS; do
    i=`basename $i`
    POST_TITLE=`grep BLOG_TITLE $BLOGDIR/$i | sed -e 's/BLOG_TITLE://;'`
    POST_DATE=`date -r $BLOGDIR/$SHOW_TARGET +"%F"`
    echo "<li><a href='$SCRIPT_NAME?show=$i'>$POST_TITLE</a> - $POST_DATE </li>"
  done
  echo "</ul>"

}

function showpost {

  FILE_DATE=`date -r $BLOGDIR/$SHOW_TARGET +"%F at %R"`
  POST=`cat $BLOGDIR/$SHOW_TARGET | sed -e 's/BLOG_KEYWORDS:.*$//g; s/BLOG_TITLE:.*$//g;'`
  KWORD_TARGET_LIST=`grep BLOG_KEYWORD $BLOGDIR/$SHOW_TARGET | sed -e 's/BLOG_KEYWORDS://;'`
  BLOG_TITLE=`grep BLOG_TITLE $BLOGDIR/$SHOW_TARGET | sed -e 's/BLOG_TITLE://;'`
  
  echo "<div class='post'> <h3>$BLOG_TITLE</h3>"
	echo "$POST"
	echo "<span class='small'>last modified at $FILE_DATE - keywords:"
	for i in $KWORD_TARGET_LIST; do
		echo "<a href='$SCRIPT_NAME?keyword=$i'>$i</a> "
	done
	echo "</span></div> <!-- post -->"

}

function showfeed {

  echo "Content-type: application/rss+xml"
  echo ""
  echo "<?xml version='1.0' encoding='UTF-8' ?> <rss version='2.0' xmlns:atom='http://www.w3.org/2005/Atom'>"
  echo "<channel><title>$TITLE</title>"
  echo "<atom:link href='http://$SERVER_NAME$SCRIPT_NAME?$QUERY_STRING' rel='self' type='application/rss+xml' />"
  if [ "x$RSS_TARGET" = "x" ]; then
    echo "<description>A weblog, primarily concerning my code dependency analysis project for Google's Summer of Code program.</description>"
  else
    echo "<description>A weblog, filtered by keyword: $RSS_TARGET</description>"
  fi
  echo "<link>http://fork.pttf.us/cgi-bin/blog.sh</link>"
  LAST_POST=`ls -t $BLOGDIR | head -1`
  LAST_BUILT=`date -Rr $BLOGDIR/$LAST_POST`
  echo "<lastBuildDate>$LAST_BUILT</lastBuildDate> <pubDate>$LAST_BUILT</pubDate>"

  for i in $MATCHING_POSTS; do
    echo "<item>"
    i=`basename $i`
    POST_TITLE=`grep BLOG_TITLE $BLOGDIR/$i | sed -e 's/BLOG_TITLE://;'`
    echo "<title>$POST_TITLE</title>"
    echo "<link>http://$SERVER_NAME$SCRIPT_NAME?show=$i</link>"
    #SNIPPET=`cat $BLOGDIR/$i | sed -e 's/^BLOG.*$//' | sed -e 'N;s/\n//;P;D;' | sed -e 's/<[^>]*>//g' | head -c 256`
    SNIPPET=`cat $BLOGDIR/$i | sed -e 's/^BLOG.*$//' | tr -d '\n' | sed -e 's/<[^>]*>//g' | head -c 512`
    echo "<description>$SNIPPET [...]</description>"
    echo "<guid>http://$SERVER_NAME$SCRIPT_NAME?show=$i</guid>"
    POST_DATE=`date -r $BLOGDIR/$SHOW_TARGET +"%F"`
    echo "<pubDate>Tue, 29 Aug 2006 09:00:00 -0400</pubDate>"
    echo "</item>"
  done
  echo "</channel>"
  echo "</rss>"

}

function endhtml {

    echo "<div style='margin-top: 5em'> &nbsp; </div>"
  echo "</div> <!-- end of container -->"

    echo "<div class='sidebar'>"
    echo "<h3>recently added/edited</h3>"
    echo "<ul>"
    FILES=`ls -t $BLOGDIR | head`
    for i in $FILES; do
      POST_TITLE=`grep BLOG_TITLE $BLOGDIR/$i | sed -e 's/BLOG_TITLE://;'`
      POST_DATE=`date -r $BLOGDIR/$i +"%F"`
      echo "<li><a href='$SCRIPT_NAME?show=$i'>$POST_TITLE</a> <br /> <span class='small'>date: $POST_DATE</span></li>"
    done
    echo "</ul> <h3>categories</h3> <ul>"
    CATEGORIES=`grep -h KEYWORD $BLOGDIR/* | sed -e 's/BLOG_KEYWORDS://g; s/ /\n/g;' | sort | uniq`
    for i in $CATEGORIES; do
      POSTCOUNT=`grep -h "KEYWORD.*$i" $BLOGDIR/* | wc -l`
      echo "<li><a href='$SCRIPT_NAME?keyword=$i'>$i</a> <span class='small'>($POSTCOUNT)</span>"
      echo "<a href='$SCRIPT_NAME?rss=$i'> <img src='/images/rss.png' alt='(rss)' /></a></li>"
    done
    echo "</ul> <h3>misc</h3>"
    echo "<ul><li><form action='$SCRIPT_NAME' method='get'><div> <input type='text' name='keyword' size='8' /> <input type='submit' value='search' /></div></form></li>"
    echo "<li><a href='http://validator.w3.org/check?uri=referer'><img src='http://www.w3.org/Icons/valid-xhtml11' alt='Valid XHTML 1.1' height='31' width='88' /></a></li>"
    echo "<li><a href='http://jigsaw.w3.org/css-validator/check/referrer'>"
    echo "<img src='http://jigsaw.w3.org/css-validator/images/vcss' height='31' width='88' alt='Valid CSS!' /></a></li>"
    echo "<li><a href='http://validator.w3.org/feed/check.cgi?url=http%3A//www.madleet.net/cgi-bin/blog.sh%3Frss%3D'>"
    echo "<img src='/images/valid-rss.png' alt='[Valid RSS]' title='Validate my RSS feed' /></a></li>"
    echo "</ul></div>"

  echo "</body></html>"

}

case $COMMAND in
  'show')
    starthtml
    if [ -r $BLOGDIR/$SHOW_TARGET ]; then
      showpost
    else
      echo "<h3 class='error'>Post not found.</h3>"
    fi
    endhtml
    ;;
  'keyword')
    starthtml
    MATCHING_POSTS=`grep -il $KWORD_TARGET $BLOGDIR/* `
    if [ "x$MATCHING_POSTS" != "x" ]; then
      keywordsearch
    else
      echo "<h3 class='error'>Nothing found for $KWORD_TARGET.</h3>"
    fi
    endhtml
    ;;
  'rss')
    if [ "x$RSS_TARGET" = 'x' ]; then
      MATCHING_POSTS=`ls $BLOGDIR/`
    else
      MATCHING_POSTS=`grep -l $RSS_TARGET $BLOGDIR/*`
    fi
    if [ "x$MATCHING_POSTS" != "x" ]; then
      showfeed
    else
      echo ""
    fi
    ;;
  *)
    SHOW_TARGET=$LATEST_POST
    echo "<h3>Latest post:</h3>"
    starthtml
    showpost
    endhtml
esac

