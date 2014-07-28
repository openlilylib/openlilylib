\version "2.16.2" % absolutely necessary!

\include "oll-base.ily"

\header {
  oll-title = "Version Number Predicates"
  oll-short-description = \markup {
    Compare against the currently running LilyPond version.
  }
  oll-author = "Urs Liska"
  oll-description = \markup \justify {
    Sometimes changes in LilyPond's syntax or behaviour cause code to be
    incompatible with a given LilyPond version. Usually this means something
    works only since or only up to a specific version. While this often can be
    treated through updating the affected input files (manually or through
    \typewriter { convert-ly}), there are situations where this isn't possible.
    It might make sense to write code that is executed conditionally
    depending on which version of LilyPond is compiling the file, for example
    in a library. An example could be the introduction of new behaviour like
    the \ollCommand temporary \ollCommand override (introduced in version 2.17.6).
    In such cases the library command can make use of the newer possibilities
    when executed from a sufficiently new LilyPond version.

    This file provides a set of predicates (or comparison operators) that you can
    use to implement conditional statements based on LilyPond version..
  }
  oll-usage = \markup \justify {
    The predicates \typewriter { lilypond-greater-than?, lilypond-greater-than-or-equal?,
    lilypond-less-than?, lilypond-less-than-or-equal? } and \typewriter lilypond-equals?
    Return a boolean value after comparing the currently run LilyPond version to the
    given argument.
    The LilyPond version has to be formatted as a three-element list, e.g.
    \typewriter { "#'(2 18 0)" } for version 2.18.0.

  }
  oll-category = "programming-tools"
  oll-tags = "control-flow,conditionals,compatibility,lilypond-version"
  oll-status = "ready"

  oll-todo = "Typechecking for the ver-list argument"
}

%%%%%%%%%%%%%%%%%%%%%%%%%%
% here goes the snippet: %
%%%%%%%%%%%%%%%%%%%%%%%%%%

#(define (calculate-version ver-list)
   ;; take a LilyPond version number as a three element list
   ;; and calculate an integer representation
   (+ (* 1000000 (first ver-list))
      (* 1000 (second ver-list))
      (third ver-list)))

#(define (lilypond-greater-than? ref-version)
   (> (calculate-version (ly:version))
      (calculate-version ref-version)))

#(define (lilypond-greater-than-or-equal? ref-version)
   (>= (calculate-version (ly:version))
       (calculate-version ref-version)))

#(define (lilypond-less-than? ref-version)
   (< (calculate-version (ly:version))
      (calculate-version ref-version)))

#(define (lilypond-less-than-or-equal? ref-version)
   (<= (calculate-version (ly:version))
       (calculate-version ref-version)))

#(define (lilypond-equals? ref-version)
   (= (calculate-version (ly:version))
      (calculate-version ref-version)))
