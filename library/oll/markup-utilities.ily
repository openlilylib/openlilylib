\version "2.16.2" % absolutely necessary!

\include "oll-base.ily"

\header {
  oll-title = "Markup Utilities"
  oll-short-description = \markup \justify {
    Utilities to format or retrieve data to be printed as text.
  }
  oll-author = "Urs Liska"
  oll-source = ""
  oll-description = \markup \justify {
    This module contains little tools and helpers to assist document authors with
    string handling. There are snippets to format and snippets to retrieve information
    as strings/markup that may be interesting to be used in titles, taglines or
    copyright fields for example.
  }
  oll-usage = \markup \justify {
    For reference concerning the use of the individual commands please refer to the
    sources of the following examples.
  }
  % add one single category.
  % see ??? for the list of valid entries
  oll-category = "markup"
  % add comma-separated tags to make searching more effective.
  % preferrably use tags that already exist (see ???).
  % tag names should use lowercase and connect words using dashes.
  tags = "string, markup, utility"
  % is this snippet ready?  See ??? for valid entries
  status = "unfinished"

  % add information about LilyPond version compatibility if available
  first-lilypond-version = ""
  last-lilypond-version = ""

% optionally add comments on issues and enhancements
  oll-todo = ""
}

%%%%%%%%%%%%%%%%%%%%%%%%
% here goes the snippet:
% Anything below this line will be ignored by generated documentation.
% The snippet itself should (usually) *not* produce any output because
% it will be included in end-user files. To provide usage examples
% please create a file with the same name but an .ly extension
% in the /usage-examples directory.
%%%%%%%%%%%%%%%%%%%%%%%%

% Format the current date as a string.
% Useful in taglines. See also the 'git-commands' file.
date = #(strftime "%d.%m.%Y" (localtime (current-time)))
