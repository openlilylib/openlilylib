\version "2.19.0"
#(ly:set-option 'strokeadjust #t)

%{
  This example includes the following notations:
  - notes with different durations
  - accidentals
  - rests
  - tempo mark
  - key signature
  - time change
  - articulations
  - dynamics
  - hairpins
  - hairpins not aligned with notes
  - lyrics
  - melismas
  - multiple instruments
  - two instruments (Soprano and Alto) sharing a staff
  - multi-staff instrument
  - polyphony
  - temporary polyphony
%}

sop = \relative f' {
  \key d \major
  a2 b cis1 b8( a g fis) a4
}

alt = \relative f' {
  \key d \major
  fis2 fis a1 b8( a g fis) fis4
}

text = \lyricmode {
  Me -- lo -- dyj -- _ ka!
}

vn = \relative f' {
  \set Staff.instrumentName = Skrzypce
  \tempo Andante 4=90
  \key d \major
  \time 4/4
  << fis1 { s2 s2\< <>\! } >>
  e2 g4 a
  \time 3/4
  d4-. c-. d-.
}

rh = \relative f' {
  \key d \major
  \time 4/4
  r d4 fis8( g a b)
  cis2 cis
  <<
    { fis4 fis fis }
    \\
    { a,2 r4 }
  >>
}

dyn = {
  s1\p\<
  s1
  s2.\f
}

lh = \relative f {
  \key d \major
  \clef F
  d2 b <a e'>1
  \time 3/4
  <d, d'>2.->
}

\score {
  <<
    \new Staff <<
      \set Staff.instrumentName = \markup \column \right-align { Sopran Alt }
      \new Voice = sop { \voiceOne \sop }
      \new Voice = alt { \voiceTwo \alt }
      \new Lyrics \lyricsto sop \text
    >>
    \new Staff \with {
      \override VerticalAxisGroup.staff-staff-spacing = #'((basic-distance . 10))
    }
    \vn
    \new PianoStaff \with { instrumentName = Pianino } <<
      \new Staff \rh
      \new Dynamics \dyn
      \new Staff \lh
    >>
  >>
  \layout {
    \numericTimeSignature
  }
  \midi {
    \set Staff.midiInstrument = clarinet
  }
}