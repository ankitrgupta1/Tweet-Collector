# Tweet-collector
This repository contains scripts which help in collecting tweets from places falling under a "Bounding Box".
"Bounding Box" is a term given to a a 4-sided geographic area. The 4 side is defined as 4 lon-lat co-ordinates of the area.
The lon-lat coordinates represents the opposite corners of the box, such that each side of the box is up to 25 miles in length. Any Tweet containing a geo Point that falls within this region will be matched. Addtionally, Tweets containing Twitter Places will match where the geo polygon defined for the Place falls fully within the defined point-radius area. Places whose polygons fall outside the defined point-radius area to any extent will not match.

Usage resembles the following: bounding_box:[west_long south_lat east_long north_lat]

Along with the collection, Tweet_Filter script will collect tweets and reformat them into a specified detailed json format.
