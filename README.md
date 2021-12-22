## Reader.py
Python script to assess the estimated read time of Red Hat Training lectures in adoc.

Usage for individual files:
> python3 reader.py <filename.adoc>

Usage for directories (automatically scan for *-lecture-content.adoc files by default):
> python3 reader.py </path/to/dir>

## cloner.py
Searches repos for courses and downloads them for use by Topic Reader

## topic_reader.py
Based on Reader.py - Searches recursively for dco.yml files. Then gets the asciidoc files lectures, GEs, and Quizzes. Each of those get a reading time calculated, and this is summed to a reading estimate by topic (in 5 minute windows). (See timing_estimates.tsv for example)

## config.ini
Edit to change consumption speeds and values.

## timing_estimates.tsv
Output is a set of tab-separated values: course, chapter, topic, estimate - data current as of November 2021
