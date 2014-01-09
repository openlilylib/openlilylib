\version "2.17.29"
\language "english"
#(ly:set-option 'relative-includes #t)
\include "Beethoven_Op10No3_notes.ly"

\layout {
  \context {
    \PianoStaff
    instrumentName = "7."
  }
}

\paper { page-count = 1 systems-per-page = 6 }

\score {
  \new PianoStaff <<
    \new Staff << \OpXNoIII_piano_global \OpXNoIII_piano_notes_upper >>
    \new Dynamics \OpXNoIII_piano_dynamics
    \new Staff << \OpXNoIII_piano_global \OpXNoIII_piano_notes_lower >>
  >>
  \header {
    title = \markup \override #'(word-space . 1) \line { S O N A T E }
    opus = "Opus 10 Nr. 3"
    dedication = "Der Gräfin Anna Margarete von Browne gewidmet"
    date = "1796/98"
  }
  \layout {
    \context {
      \Score
      \consists #(bars-per-line-systems-per-page-engraver '((6*2 5*4)))
      \override NonMusicalPaperColumn.line-break-permission = ##f
      \override NonMusicalPaperColumn.page-break-permission = ##f
    }
  }
}