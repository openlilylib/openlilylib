\version "2.18.0"

% This will for example load the definitions file with the same basename.
\include "oll-usage-example.ily"

% Activate devMode
\devModeOn

\markup \section { First example }

\markup \justify {
  Describe the usage example(s) in detail
}

\score {
  <<
    \new Staff \relative fis' {
      fis fis g a a g fis e
    }
    \new Lyrics \lyricmode {
      Freu -- de, schö -- ner Göt -- ter -- fun -- ken
    }
  >>
}


\score {
  <<
    \new Staff \relative fis' {
      fis fis g a a g fis e
    }
    \new Lyrics \lyricmode {
      \lyrLeft Freu -- \lyrRight de, schö -- ner Göt -- ter -- fun -- ken
    }
  >>
}