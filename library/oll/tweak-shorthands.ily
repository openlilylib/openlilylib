\version "2.16.2" % absolutely necessary!

\include "oll-base.ily"

\header {
  oll-title = "Tweak shorthands"
  oll-short-description = \markup {
    Shorthands for regular tweaking operations
  }
  % provide a comma-separated list to credit multiple authors
  oll-author = "Janek Warchoł, Urs Liska"
  oll-source = ""
  oll-description = \markup \justify {
    Despite the goal of providing \italic {automatic engraving} it is
    regularly necessary to apply manual tweaks. This module provides a
    number of "\"generic\"" tweaks to save typing and increase consistency.
    Apart from that they benefit from the \typewriter devMode concept.
  }
  % add one single category.
  % see ??? for the list of valid entries
  oll-category = "none"
  % add comma-separated tags to make searching more effective.
  % preferrably use tags that already exist (see ???).
  % tag names should use lowercase and connect words using dashes.
  oll-tags = ""
  % is this snippet ready?  See ??? for valid entries
  oll-status = ""

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


% TODO: add oll/snippets headers, add example.
% split into several files
% update syntax to 2.18?


%{
  Move note heads right or left to avoid
  collisions or NoteColumn clashes
  Use of \moveNote is preferred over manual tweak of #'force-hshift
  because the tweak is colored in draftMode
%}

moveNote =
#(define-music-function (parser location amount)
   (number?)
   (if dev-mode
       #{
         \once \override NoteColumn #'force-hshift = #amount
         \once \override NoteHead #'color = #dev-mode-color-tweak
       #}
       #{
         \once \override NoteColumn #'force-hshift = #amount
       #}))


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Move a rest up or down when LilyPond doesn't do the right thing

restPos =
#(define-music-function (parser location staff-position)
   (integer?)
   (if dev-mode
       #{
         \once \override Rest #'staff-position = #staff-position
         \once \override Rest #'color = #dev-mode-color-tweak
         \once \override MultiMeasureRest #'staff-position = #staff-position
         \once \override MultiMeasureRest #'color = #dev-mode-color-tweak
       #}
       #{
         \once \override Rest #'staff-position = #staff-position
         \once \override MultiMeasureRest #'staff-position = #staff-position
       #}))


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

beampos =
#(define-music-function (parser location pos)
   (pair?)
   #{
     \once \offset Beam #'positions #pos
   #})

staffdist =
#(define-music-function (parser location distances)
   (list?)
   #{
     \overrideProperty #"Score.NonMusicalPaperColumn"
     #'line-break-system-details
     #(list (cons 'alignment-distances distances))
   #})

tieconf =
#(define-music-function (parser location conf)
   (list?)
   #{ \once \override TieColumn #'tie-configuration = #conf #})

extraoff =
#(define-music-function (parser location val mus)
   (number-pair? ly:music?)
   #{
     \tweak #'extra-offset #val #mus
   #})

stemlen =
#(define-music-function (parser location val)
   (number?)
   #{
     \once \override Stem #'length = #val
   #})

padding =
#(define-music-function (parser location grob padding)
   (string? number?)
   #{
     \once \override $grob #'padding = #padding
   #})

tweakPadding =
#(define-music-function (parser location padding mus)
   (number? ly:music?)
   #{
     \tweak #'padding #padding #mus
   #})

positions =
#(define-music-function (parser location grob positions)
   (string? pair?)
   #{
     \once \override $grob #'positions = #positions
   #})

whiteout =
#(define-music-function (parser location mus)
   (ly:music?)
   #{
     \tweak #'whiteout ##t #mus
   #})

xoff =
#(define-music-function (parser location val mus)
   (number? ly:music?)
   #{
     \tweak #'X-offset #val #mus
   #})

yoff =
#(define-music-function (parser location val mus)
   (number? ly:music?)
   #{
     \tweak #'Y-offset #val #mus
   #})

xyoff =
#(define-music-function (parser location xval yval mus)
   (number? number? ly:music?)
   #{
     \tweak #'X-offset #xval \tweak #'Y-offset #yval #mus
   #})
