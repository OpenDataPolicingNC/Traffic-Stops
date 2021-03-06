The traffic stop data received from the state of Maryland has been post-processed
in two general ways:

- Add 2016 YTD Excel worksheet as-is to pre-2016 Excel workbook.  See the
  README in the dataset for more information.
- Address minor variations in the input data as well as group values into a
  smaller set of categories for display in the web interface.  These changes
  are described below for columns where such processing is performed.

TIME_OF_STOP
------------

A small number of values for this field are not valid times.  Any time which is
not valid is treated as 00:00 (midnight).  Thus, some traffic stops will be
treated as occurring at midnight even though they happened at a different time
on that day.

Example invalid values: ":", "24:44"

STOP_REASON
-----------

The input data consists of code references like "13-411(f)", "13-411", "21-801.1",
"64*", and so on.  This is transformed to a stop purpose, like 'Seat Belt Violation',
'Driving While Impaired', and so on.  A spreadsheet provided by SCSJ maps stop
reasons (codes) to the various purposes.  The codes are simplified in the spreadsheet
reflecting that subsections, paragraphs, etc. aren't relevant to the mapping, so
the raw stop codes are similarly simplified before looking them up.

After transforming to a stop purpose, stop data for these purposes is removed from
the dataset:

- "Investigation"
- "Failure to remain at scene of accident"

Here are typical examples of how the raw data values from MD are simplified
before matching with values in the spreadsheet:

- ``64*`` => ``64``
- ``21-202(h1)`` => ``21-202``
- ``21-507G3I(i1)`` => ``21-507``
- ``22-412.3(c2)`` => ``22-412``
- ``409-b`` => ``409``
- ``412.3-b`` => ``412``

The SCSJ was originally provided as an Excel worksheet; it was saved as CSV from
LibreOffice.  The spreadsheet is in this repository as
``md/data/STOP_REASON-normalization.csv``.

GENDER
------

A small number of stops do not have a gender recorded.  Additionally, a handful
of stops do not have recognizable values for gender recorded.  These are treated
as Unknown.

Example invalid values: "MD", "n"

SEIZED
------

Both personal property and contraband can be seized, but for the purposes of this
web site only the seizure of contraband is considered.

Any stop with a SEIZED field value starting with "Contraband" or the words "Both"
or "paraphernalia" is treated as having an item seized.

Example values which are not treated as seizure of contraband: "N/A", "Property Only",
"No CDs in vehicle", "28124", "arrest", "impound inventory".

ETHNICITY
---------

All values of the ETHNICITY column have been mapped to one of

  WHITE, BLACK, HISPANIC, ASIAN, NATIVE AMERICAN, UNKNOWN

Most values of ETHNICITY are already one of these values.  If the data recorded
is "OTHER" or blank or an unrecognized value, it is treated as UNKNOWN.

Example invalid values: "M", "F", "hiq"

Age, as computed from STOPDATE and DOB
--------------------------------------

If the DOB is after STOPDATE, age is treated as zero.
