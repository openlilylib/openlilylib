\version "2.16.2" % absolutely necessary!

\header {
  oll-title = "Predicates for LilyPond version numbers"
  oll-short-description = \markup {
    Compare the currently running LilyPond version
    against a given version.
  }
  oll-author = "Urs Liska"
  oll-description = \markup {
    This snippet provides a set of predicates (or comparison
    operators) for LilyPond version numbers.
    This is useful for implementing switches in functions
    to execute code depending on the LilyPond version
    that is currently running.

    The functions take a LilyPond version number (formatted
    as a three element list) as argument and
    compare that to the version number of the running LilyPond.
  }
  oll-category = "helpers"
  oll-tags = "control-flow,conditionals,compatibility,lilypond-version"
  oll-status = "ready"

  oll-todo = "Typechecking for the ver-list argument"

  oll-custom = "Test"
  oll-custom-2 = \markup {
    Test
    and go
  }
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
