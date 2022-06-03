NetVision API README


GENERAL INFORMATION

1. Overview of Program Functionality 

This program allows for someone to mine social media network data from Reddit.
Given a specific topic of interest, someone can find the subreddits where the
topic is being discussed, the posts in each of those subreddits about that topic,
internal links between subreddits on the topic and external links between Reddit
and other social media platforms (plus news sites, etc.). In addition, metrics for
each of these levels of investagation are also gathered and presented in tabular
and (eventually) graphical format. Specific details on functions can be found
in section 6 of this readme.

2. What Does this Program Offer that Others Don't?

The major "value add" of this program is that it extracts additional data not
immediately available in the json returned from an API call. It also focuses
on presenting data relevant to a network investigation/analysis. It also may
operate more quickly/efficiently than some other tools out there. Specifically,
this program:

-mines links embedded in the text of a subreddit post
-calculates additional features, such as the liftime of a post
-aggregates data about network connections
-allows for exploration of a specific topic rather than generic subreddit data

3. Current Key Limitations of Program

Currently, the maximum number of posts that can be returned is 1000 "deep" of
whatever search is being done. So, for example, from time, NOW, only the last
1000 posts can be gathered. For looking at the most popular posts, only the 1000
most popular posts can be grabbed, etc. (the actual number is always somewhere
between 900 and 1000). This is a hard limit imposed by the Reddit API itself.
Any one query is limited to 100 results. To get more than 100 results, the id of
the last query is used as a starting point for an additional query, and so on,  
but the hard limit comes in around 1000. This limits any reasarch done
with this program to current and future occurances. Historical data cannot be
gathered. However, one could use this program to systematically gather data once 
some new issue/topic of interest emerges.

That being said, one can go to this website:

https://subredditstats.com/r/ukraine

which has been gathering general metrics on subreddits for a number of years in
order to get some awarness of historical data. It is also a good launching
point/comparative tool for any investigation inovloving Reddit.

The API also seem to have a "cutoff" for subreddit searches around ~60 subreddits.
Running multiple queries using the last subreddit id of the previous query worked,
but did not return any more queries above the ~60 mark. Thus it is only useful to
do a single subreddit search with the result limit set to the API maximum of 100.

When searching for corssposts, the duplicates endpoint never seems to return the
full number of crossposts as reported in the posts dataframe. Sometimes the number
of crossposts returned was far below the number reported for the post. Additionally,
there is occasionally a 504 error (timeout) connection error with the Reddit server.
When this is the case, changing the limit parameter to 50 and bracketing up
from there, worked as a (non-ideal) solution. However, in such cases ~55 seemed to
be the maximum limit the server could handle before timing out.

4. Adaptions and Future Updates

It is intended that the user employ the "create_[some type of dataframe]()" functions
in this program. This will do all the work of gathering the data from the API,
extracting it, and creating and displaying a dataframe of variables pre-assessed as
valuable for network analysis. That being said, the user has access to the "helper"
functions and can modify any aspect of the investigation. The "get_[some type of]_json()"
functions access specific endpoints in the reddit API. If desired, these functions can
be used to grab the data and the user can build/modify functions to extract the specific
json objects/data that they want. By examing the Reddit API documentation on its dozens
of endpoints (https://www.reddit.com/dev/api/), the user can also modify a
"get[some type of]_json()" function to mine an endpoint not covered in this program.  

Looking forward whilst weilding the magic wand, it is desired to build additional functions
to cover more of the Reddit API endpoints. Adding in functions that displayed the data
visually would enhance things greatly too. The limitations encounted in this version would
also be thoroughly investigated to at least uncover the cause, and hopefully find a 
work-around. Additionally, the endpoints return json files with many dozens of data points,
many of which have little or no documenatation anywhere. A deep investgation of all these
data points, leading to detailed doucumentation, could also be done. It may also be worthwhile
to pursue building this program out as a proper piece of software, complete with a user 
interface and full funcionality, such that totally non-techincal users could do work with it.
Additionally, improving the aggregate functions so that the can add all the links for all of
the subreddits at the same instead of doing one subreddit at a time would be good.

Most importantly, adding scripts that automate calls to the Reddit API are critically needed.
It seems likely that, due to hard limitations that appear to exist accessing the API, in order
to gather data for longitudinal studies, such automated regular calls are needed. Along those
lines, building some dashboards that store historical data could be benefical.

USING THE PROGRAM

5. Setting up Access to Reddit

To set up access tp the Reddit API up, you will need to provide some information.
First, you will need to obtain an api app from reddit.

Instructions for how to do so can be found here:
https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c

You only need to complete sections 1-3 in this article.
Once you complete steps 1-3 in the article, you will have a Reddit:

-personal use script
-secret

Now, you need to create a "credentials" text file that will be used to read in the
necessary information to access the Reddit API. This credentials file wil also
include your Reddit username and password. It should have the following format:

Credentials
(insert your api app personal script)
(insert your api app secret)
(insert your username)
(insert your password)

It is important that the credentials file be in this format, or the program will
encounter an error when attempting to authneticate and connect to the Reddit API.
It is also important that you store this credentials file in the same directory
you will be working from when you use this program. If an error occurs, please
read the error message and make appropriate corrections.

From here you will need to grab your working directory:
directory=os.getwd()

Then feed in your credentials from your credentials text file:
credentials_df=load_credentials(direcotry, file_name)

Finally, you need to use this information to authenticate and connect to the API:

headers=connect_to_api(credentials_df)

Note that this will return a headers dictionary. This headers dictionary contains the
authorization token and other needed details for using the API endpoints. It should
be left alone.

You are now ready to mine network data from Reddit!

6. The (Most Important) Function Details

A few general notes:
Subreddits, posts, comments, etc. all have different "tn_" designaters in Reddit.
Some of thes functions in this program require passing arguments of a post ID.
Please ensure that the variable being passed has the appropriate "tn_" designator.
For exmaple, posts are t3_(id string). All of the dataframes returned by these
functions will have correct ids listed for all observations, should any of those 
observations be used for further investigation. One excpetion to this rule is that
when searching for crossposts, the original post's id should be passed WITHOUT the
t3_ designator.

Generally, if the subreddit is needed as a parameter for a function, the NAME of
the subreddit is used, as opposed to its t1_id.

More information can be found in the Reddit API documentation. Near the top, look
for the "fullnames" and "type prefixes" headers:
https://www.reddit.com/dev/api/

Also- it is highly reccommended that you use the display() function from Ipython.display
(as oppossed to print()) to show the dataframes.

A. create_subredditsDF(params,headers)

This function returns a pandas DF of the subreddits which contain posts on the
given topic of interest. A dictionary of parameters is passed to the function
which will guide the Reddit API in what it looks for exactly. 

Reddit API documenation for search endpoint parameters:
https://www.reddit.com/dev/api/#GET_search

The most important parameters are the following:
q:     the actual wording of the query. For example: "Dow Jones crash"
limit: the maximum number of results (subreddits) to return. This is
       the number of results returned per query. 100 is the maxium.
type:  this designates the object to search in Reddit. For subreddits, "sr" is
       used. This should be left alone, otherwise an error will occur.
sort:  how the search will order the results. The default used in this program
       is "relevance"
t:     timeframe in which to look for the results. Doesn't seem to effect
       searches of subreddits, but set to "all" for safety.

Internally, it calls two other functions:
-get_subreddits_json()
-extract_sr_data()

The first connects to the API and pulls the data.
The second extracts the desired data into a dataframe.
Either of the two internal functions can be used indendently if you so desire.

Dataframe fields:
subreddit-        the name of the subreddit
subreddit_id-     the id of the subreddit (proceeded by t5_)
type-             whether a public or private subreddit
url-              the url of the subreddit, append on the end of reddit.com
title-            generally used to describe the subreddit
description-      often blank, or used to descrube subreddit
creation_date-    time subreddit was created (utc)
subscribers-      number of subscribers to subreddit
submit_text-      instructions/rules for submitting a post


B. create_postsDF_by_topic(sr,params,n,headers)

This function returns a pandas DF of the posts in a given subreddit related to
the specificed topic of interest. The subreddit NAME to search will need to be
provided (sr). Additionally, the parameters dictionary will have some important
criteria for the search.

Importantly, the arugment, "n", is also passed to the function. In order to
get more than 100 results, multiple queries will need to be carried out. The
final amount of results returned from the function will be n*limit. It should
be noted, however, that as discussed in Section 3 on limitations of the
program, there is a hard cutoff around ~1000 results, regardless of how many
queries are used. 

Reddit API documenation for search endpoint parameters:
https://www.reddit.com/dev/api/#GET_search

The most important parameters are the following:
q:     the actual wording of the query. For example: "Dow Jones crash"
limit: the maximum number of results (subreddits) to return. This is
       the number of results returned per query. 100 is the maxium.
type:  this designates the object to search in Reddit. For posts "link" is
       used. This should be left alone, otherwise an error may occur.
sort:  how the search will order the results. The default used in this program
       is "relevance"
restrict_sr:  This should be set to True to only search the given subreddit.
              Otherwise, all of Reddit will be searched
			  
Internally, it calls two other functions:
-get_posts_by_topic_json()
-extract_posts_data()

The first connects to the API and pulls the data.
The second extracts the desired data into a dataframe.
Either of the two internal functions can be used indendently if you so desire.

Dataframe fields:
author_username-  the username of the poster
author_id-        the id of the post (proceeded by a t_2)
post_id-          the id of the post (a "link")
title-            the title of the posts
text-             the text of the post
flair-            generally denotes the category of post, for example, "News"
url-              the url that the media is sourced from
permalink-        where to find the post on reddit (add to the end of reddit.com)
subreddit-        the name of the subreddit
subreddit_id-     the id of the subreddit (proceeded by t5_)
post_creation-    time post was made (utc)
original-         whether or not is original content (needs more investigation)
domain-           where the post is sourced from (Reddit, or other social media)
score-            net of upvotes - downvotes
upvote_ratio-     % of votes that were upvotes
comments-         how many comments the post has received
crosspostable-    boolean, whether or not the post can be crossposted
crossposts-       the number of times the post has been crossposted

C. create_postsDF_by_sort_type(sr,sort_type,params,n,headers)

This function returns a pandas DF of the posts in a given named subreddit (sr),
sorted by the chosen method. This will not filter for posts pertaining to the
given topic of interest but sorts all posts by the given criteria. A dictionary
of parameters is passed to the function which will guide the API in its search. 

Importantly, the arugment, "n", is also passed to the function. In order to
get more than 100 results, multiple queries will need to be carried out. The
final amount of results returned from the function will be n*limit. It should
be noted, however, that as discussed in Section 3 on limitations of the
program, there is a hard cutoff around ~1000 results, regardless of how many
queries are used. 

Reddit API documenation for search endpoint parameters:
https://www.reddit.com/dev/api/#GET_{sort}

The most important parameters are the following:
limit: the maximum number of results (subreddits) to return. This is
       the number of results returned per query. 100 is the maxium.
t:     timeframe in which to look for the results.

Internally, it calls two other functions:
-get_posts_by_sort_type_json()
-extract_posts_data()

The first connects to the API and pulls the data.
The second extracts the desired data into a dataframe.
Either of the two internal functions can be used indendently if you so desire.

Dataframe fields:
author_username-  the username of the poster
author_id-        the id of the post (proceeded by a t_2)
post_id-          the id of the post (a "link")
title-            the title of the posts
text-             the text of the post
flair-            generally denotes the category of post, for example, "News"
url-              the url that the media is sourced from
permalink-        where to find the post on reddit (add to the end of reddit.com)
subreddit-        the name of the subreddit
subreddit_id-     the id of the subreddit (proceeded by t5_)
post_creation-    time post was made (utc)
original-         whether or not is original content (needs more investigation)
domain-           where the post is sourced from (Reddit, or other social media)
score-            net of upvotes - downvotes
upvote_ratio-     % of votes that were upvotes
comments-         how many comments the post has received
crosspostable-    boolean, whether or not the post can be crossposted
crossposts-       the number of times the post has been crossposted

D. create_xsposts_df(sr,article,params,headers)

This function returns a pandas DF of the crossposts of the given post. It is
necessary to pass the NAME of the subreddit to find the original post in (sr)
and the id of the post to look for crossposts of (article). A dictionary of
parameters is passed to the function which will guide the API's search. 

NOTE - unlike every other instance of passing an object's id, in this case,
the id of the original post (article) should be passed to the function WITHOUT
the t3_ designator.

Reddit API documenation for search endpoint parameters:
https://www.reddit.com/dev/api/#GET_duplicates_{article}

The most important parameters are the following:
limit: the maximum number of results (subreddits) to return. This is
       the number of results returned per query. 100 is the maxium.

Dataframe fields:

parent_post_id-       the id of the orginal post
parent_subreddit-     the name of the subreddit the original post comes from
parent_subreddit_id-  the id of the subreddit the original post comes from
xposter_username-     the username of the crossposter
xposter_id-           the id of the crossposter (proceeded by a t_2)
xpost_id-             the id of the crosspost (a "link")
title-                the title of the crossposts
text-                 the text of the crosspost
flair-                generally denotes the category of crosspost, for example, "News"
url-                  the url that the media is sourced from
permalink-            where to find the crosspost on reddit (add to the end of reddit.com)
subreddit-            the name of the subreddit where the crosspost is located
subreddit_id-         the id of the subreddit where the crosspost is located (proceeded by t5_)
subreddit_type-       whether the subreddit where the crosspost is located is public or private
subreddit_subs-       the number of subscribers to the subreddit where the crosspost is located
xpost_creation-       time crosspost was made (utc)
original_creation-    whether or not crosspost is original content (will always be False!)
elapsed_time_days-    time from original post creation to crosspost creation ("lifetime" of original post)
edited-               whether the original post was edited
domain-               where the crosspost is sourced from (should always be a Reddit domain)
ups-                  total up votes crosspost received
downs-                total down votes the crosspost received
score-                net of upvotes - downvotes
upvote_ratio-         % of votes that were upvotes
comments-             how many comments the crosspost has received
crosspostable-        boolean, whether or not the crosspost can be crossposted
crossposts-           the number of times the crosspost has been crossposted

E. create_ext_link_df(df)

This function takes the posts from a given subreddit and looks at the domain
column, which is where the post is sourced from. The source could be internal
to Reddit, or from some external platform. The function determines which links
are externally sourced. Then it tallies up how many links there are per source
and returns a dataframe of this information.

Dataframe fields:
author_username-   the username of the poster
author_id-         the id of the post (proceeded by a t_2)
post_id-           the id of the post (a "link")
title-             the title of the posts
text-              the text of the post
flair-             generally denotes the category of post, for example, "News"
url-               the url that the media is sourced from
permalink-         where to find the post on reddit (add to the end of reddit.com)
subreddit-         the name of the subreddit
subreddit_id-      the id of the subreddit (proceeded by t5_)
post_creation-     time post was made (utc)
original-          whether or not is original content (needs more investigation)
domain-            where the post is sourced from (will always be non-Reddit)
score-             net of upvotes - downvotes
upvote_ratio-      % of votes that were upvotes
comments-          how many comments the post has received
crosspostable-     boolean, whether or not the post can be crossposted
crossposts-        the number of times the post has been crossposted

F. mine_text_links(df)

This function mines the text of posts from a given subreddit for links. It also
checks to see if any links are duplicate links if there are multiple links in
a single post. All the links are tallied up and a dataframe created of the sources
of the links (both external and internal) and the number of links per source.

Dataframe fields:
domain-            the source of the link (this is actually the index of the DF)
total_links-       number of links for that domain
parent_sr-         the name of the subreddit these links are found in
parent_sr_id-      the id of the subreddit these links are found in

G. The various, aggregate_[some kind of link]_to_df(sr_df, df):

There are three types of this function. One that calculates the number of links that
are explicitly made from external sources (that is, posts that are not sourced from
Reddit), a seconf that finds internal links (that is crossposts connecting one subreddit
to another) and one that tallies text links (which can be either internal or external).
All of them work by taking in a dataframe of the most recent posts in a given subreddit,
determining the type of link and tallying up how many of them there are. Then, that
information is posted back to the subreddits dataframe, with the number of external
and/or internal links being updated for the given subreddit.

Fields added to a dataframe:
external_domain_links-        the number of links for non-Reddit sources
internal_links-               the number of links to other subreddits