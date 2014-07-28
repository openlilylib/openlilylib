\version "2.16.0"

\include "oll-usage-example.ily"


versionCommentA =
#(define-music-function (parser location ver)
   (list?)
   (cond ((lilypond-greater-than-or-equal? ver)
          #{ s^\markup {#(lilypond-version) is higher or equals that.} #})
         ((lilypond-less-than-or-equal? ver)
          #{ s^ \markup {#(lilypond-version) is less or equals that.} #})))

versionCommentB =
#(define-music-function (parser location ver)
   (list?)
   (cond ((lilypond-greater-than? ver)
          #{ s^\markup {#(lilypond-version) is higher} #})
         ((lilypond-equals? ver)
          #{ s^\markup {#(lilypond-version) is equal} #})
         ((lilypond-less-than? ver)
          #{ s^\markup {#(lilypond-version) is less} #})))

\markup \section {Examples:}

\markup \justify {
  To use the provided predicates you should define a music function which
  contains an \typewriter if or a \typewriter cond expression and return
  different content depending on the result of th predicate.
  Compile this file with different versions of LilyPond
  and see how the output markups change. If the file is outdated (i.e. \italic
  all your LilyPond versions are newer than the ones compared with) feel free
  to change the versions used as comparisons in the example.
}

\markup { \vspace #3 }

\markup \bold { Compiled with LilyPond #(lilypond-version) }

\markup { \vspace #3 }

{
  \tempo "Comparing with: 2.18.0"
  s1
  \versionCommentA #'(2 18 0)
  \versionCommentB #'(2 18 0)
}

\markup { \vspace #2 }

{
  \tempo "Comparing with: 2.18.2"
  s1
  \versionCommentA #'(2 18 2)
  \versionCommentB #'(2 18 2)
}

\markup { \vspace #2 }

{
  \tempo "Comparing with: 2.19.5"
  s1
  \versionCommentA #'(2 19 5)
  \versionCommentB #'(2 19 5)
}

\markup { \vspace #2 }

{
  \tempo "Comparing with: 2.19.16"
  s1
  \versionCommentA #'(2 19 16)
  \versionCommentB #'(2 19 16)
}
