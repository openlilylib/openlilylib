\version "2.19.0"
#(ly:set-option 'strokeadjust #t)

sop = \relative f' {
  \key d \major
  a2 b cis1 b8( a g fis) a4
}

alt = \relative f' {
  \key d \major
  fis2 fis a1 b8( a g fis) fis4
}

text = \lyricmode {
  Ach, cóż za ra -- dość!
}

vn = \relative f' {
  \set Staff.instrumentName = Skrzypce
  \tempo Andante 4=90
  \key d \major
  \time 4/4
  d4-.\p c-.d-.c-.
  e2(\< g4 a)
  \time 3/4
  d2.\f
}

vc = \relative f {
  \set Staff.instrumentName = Wiolonczela
  \tempo Andante 4=90
  \key d \major
  \clef F
  d2\mf b <a e'>1
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
    \new StaffGroup <<
      \new Staff \with {
        \override VerticalAxisGroup.staff-staff-spacing = #'((basic-distance . 11))
      }
      \vn
      \new Staff \vc
    >>
  >>
  \layout {
    \numericTimeSignature
  }
  \midi {
    \set Staff.midiInstrument = clarinet
  }
}