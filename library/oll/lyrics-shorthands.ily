\version "2.16.2" % absolutely necessary!

\include "oll-base.ily"

\header {
  oll-title = "Lyrics shorthands"
  oll-short-description = \markup {
    Shorthands for regular lyrics tasks
  }
  oll-author = "Janek Warchoł, Urs Liska"
  oll-source = ""
  oll-description = \markup \justify {
    Manual alignment of lyrics is simple but somewhat tedious. This file
    contains a number of shorthands to reduce the necessary amount of typing.
    Additionally there are shorthands for melisma handling.
  }
  % add one single category.
  % see ??? for the list of valid entries
  oll-category = "input-shorthands"
  % add comma-separated tags to make searching more effective.
  % preferrably use tags that already exist (see ???).
  % tag names should use lowercase and connect words using dashes.
  tags = "lyrics,alignment,melisma"
  % is this snippet ready?  See ??? for valid entries
  status = "ready"

  % add information about LilyPond version compatibility if available
  first-lilypond-version = ""
  last-lilypond-version = ""

  % optionally add comments on issues and enhancements
  oll-todo = "This could be extended"
}

%%%%%%%%%%%%%%%%%%%%%%%%
% here goes the snippet:
% Anything below this line will be ignored by generated documentation.
% The snippet itself should (usually) *not* produce any output because
% it will be included in end-user files. To provide usage examples
% please create a file with the same name but an .ly extension
% in the /usage-examples directory.
%%%%%%%%%%%%%%%%%%%%%%%%



%%%%%%%%%%%%%%
% Align lyrics

lyrAlign =
#(define-music-function (parser location amount)
   (number?)
   (if dev-mode
       #{
         \once \override LyricText #'self-alignment-X = #amount
         \once \override LyricText #'color = #dev-mode-color-tweak
       #}
       #{
         \once \override LyricText #'self-alignment-X = #amount
       #}))

lyrLeftI =      \lyrAlign #0.2
lyrLeftII =     \lyrAlign #0.4
lyrLeftIII =    \lyrAlign #0.6
lyrLeftIIII =   \lyrAlign #0.8
lyrLeft =       \lyrAlign #1

lyrRightI =     \lyrAlign #-0.2
lyrRightII =    \lyrAlign #-0.4
lyrRightIII =   \lyrAlign #-0.6
lyrRightIIII =  \lyrAlign #-0.8
lyrRight =      \lyrAlign #-1


%{Set melisma behaviour
   Some composers (e.g. Oskar Fried) don't use slurs and beams
   accordings to the standards, so one has to deal with melismaBusyProperties
   - for which the two commands offer shorthands.
   Generally melOn should be active vor vocal melodies,
   so ties, slurs and beams cause a melisma.
   If the lyrics proceed under ties, slurs or beams,
   melOff has to be activated.
   The command has to be placed after the beginning of the syllable
%}
melOff = {
  \set melismaBusyProperties = #'()
}
melOn = {
  \unset melismaBusyProperties
}
