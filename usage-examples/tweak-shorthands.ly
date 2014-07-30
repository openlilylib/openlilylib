\version "2.16.2"

\include "oll-usage-example.ily"

\markup \section \ollCommand "moveNote #-0.5"

\markup \justify {
  Shift the notecolumn right or left, can be used to avoid clashing note heads.
  \italic Note: This affects the note\italic column, not the note \italic head. So
  if you experience problems with this function check whether the two notes share
  the same notecolumn. Usually this is because they are assigned the same voice
  number. And often fixing this makes the use of \ollCommand moveNote obsolete.
}

\relative c'' {
  <<
    { \voiceOne c b a b c1 } \\
    \new Voice {
      \voiceTwo a4 g f \moveNote #-0.5 f e1
    }
  >>
}

\markup \section \ollCommand "restPos"

\markup \justify {
  Manually position a rest to a staff position, passing an iteger argument.
  "#0" means the middle staff line, positive numbers are above, negative numbers
  below this line. Note that you can achieve the same effect with named rests
  (e.g. \typewriter {"c4\\rest"}, but depending on the situation this function
  may be better suited to what you want to achieve.
}

\relative c'' {
  r4
  \restPos #1 r
  \restPos #-1 r
  \restPos #0 r
  R1
  \restPos #-3 R1
}