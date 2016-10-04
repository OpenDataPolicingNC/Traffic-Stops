The traffic stop data received from the state of Illinois was post-processed
as described below to facilitate display on the web interface.

"agencyname" column
-------------------

The same agency may be written in multiple variations such as
"ABINGDON POLICE" and "ABINGDON POLICE DEPARTMENT".  The first variation
encountered in the dataset is the one used for display, after converting to
mixed case.

"Race" column
-------------

The input data uses the code "O" for "other".  This code is imported as "U"
and the web interface refers to it as "unknown".

"Search" column
---------------

Many entries have no value for this column instead of a "Y" or "N".  Those
with no value are imported as "U" and the web interface refers to it as
"unknown".

"Contraband" column
-------------------

Many entries have no value for this column instead of a "Y" or "N".  Those
with no value are imported as "U" and the web interface refers to it as
"unknown".

This field is referred to as "seized" in the web interface.

Census data
-----------

A spreadsheet is used to map agencies to census locations.  The initial
mapping was created by removing "Police" or "Police Department" from the
end of agency names and then attempting to match the remainder of the
agency name to a city, town, or village in the census data.  Many agencies
match a census location.
