\version "2.19.0"
#(ly:set-option 'strokeadjust #t)

%{
  This example includes the following notation elements:

  Basics:
  - pitches
  - chords
  - accidentals
  - different durations
  - dotted durations
  - rests
  - single-note articulations
  - spanner articulations (slurs)

  Structural:
  - tempo mark
  - key signature
  - time change
  - multiple instruments
  - multi-staff instrument
%}

vn = \relative f' {
  \set Staff.instrumentName = Skrzypce
  \tempo Andante 4=90
  \key d \major
  \time 4/4
  fis1
  e2 g4 a
  \time 3/4
  d4-. c-. d-.
}

rh = \relative f' {
  \key d \major
  \time 4/4
  r d4 fis8( g a b)
  cis2 cis
  <fis, a fis'>4 r2
}

lh = \relative f {
  \key d \major
  \clef F
  d2 b <a e'>1
  \time 3/4
  <d, d'>2.
}

\score {
  <<
    \new Staff \vn
    \new PianoStaff \with { instrumentName = Pianino } <<
      \new Staff \rh
      \new Staff \lh
    >>
  >>
  \layout {
    \numericTimeSignature
    \override Score.SpacingSpanner #'common-shortest-duration = #(ly:make-moment 1 8)
  }
  \midi {
    \set Staff.midiInstrument = clarinet
  }
}