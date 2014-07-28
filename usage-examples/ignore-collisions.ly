\version "2.16.2"

\include "oll-usage-example.ily"

\markup \justify {
  The following example demonstrates one possible technique to create a
  (faked) cross-voice tie. In this implementation we flip the first
  \typewriter { c'' }'s stem downwards to give the impression of a chord.
  But this will make that note share the note column with the \typewriter
  { < e' g'> }, thus producing the compiler warning.
}


\relative c'' {
  <<
    {
      \voiceTwo
      c2 ^~ \voiceOne c4. b8
    } \\
    \new Voice {
      \voiceTwo
      <e, g>2 <d f>
    }
  >>
}

\markup { Using \ollCommand ignoreCollision will suppress this warning }

\relative c'' {
  <<
    {
      \voiceTwo
      \ignoreCollision
      c2 ^~ \voiceOne c4. b8
    } \\
    \new Voice {
      \voiceTwo
      <e, g>2 <d f>
    }
  >>
}

\markup {
  Of course you will only notice the difference when actually \italic
  compiling this file.
}