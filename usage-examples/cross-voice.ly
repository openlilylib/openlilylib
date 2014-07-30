\version "2.18.0"

\include "oll-usage-example.ily"

\devModeOn

\markup \justify {
  The following examples demonstrate possible approaches to create a
  (faked) cross-voice tie (for another technique see \ollRef ignore-collisions).
  The first image shows what happens when using \ollCommand hideNotes: we get
  a crippled tie (printed in red) which tries to avoid the invisible flag of
  the hidden upper \typewriter {c''}.
}

\relative c'' {
  \partial 8*5
  <<
    {
      \hideNotes
      \once \override Tie.color = #red
      c8 ^~
      \unHideNotes
      c4. b8
    } \\
    \new Voice {
      \voiceTwo
      <e, g c>8 <d f>
    }
  >>
}

\markup \justify {
  The next version is probably the one used most: add a hidden note at one end of
  the cross-voice item you want to print. For this simply write \ollCommand
  \concat {"hideVoiceForCrossVoice " <grobname>} before the note \italic starting
  the element. When \typewriter devMode is active both the note and the element are
  colored using \typewriter dev-mode-color-switch.
}

\relative c'' {
  \partial 8*5
  <<
    {
      \hideVoiceForCrossVoice Tie
      c8 ^~ c4. b8
    } \\
    \new Voice {
      \voiceTwo
      <e, g c>8 <d f>
    }
  >>
}

\markup \justify {
  However, sometimes you can't integrate the hidden note in the actual voice
  (like in the following example where the \typewriter f' happens at the same
  time as the \typewriter c'').
  Then you can print the cross-voice element in a voice on its own, making use
  of the fact that the function actually accepts a music expression as its second
  argument. That means when you enclose anything in curly braces after the function
  and the grobname argument it will be treated as a hidden voice completely.
}

\relative c'' {
  \partial 8*5
  <<
    {
      s8
      \hideVoiceForCrossVoice Glissando {
        % The whole music expression is treated as the hidden voice now.
        \voiceTwo f,8 \glissando
        s4
        \voiceOne b8
      }
    }
    \new Voice {
      \voiceOne
      \hideVoiceForCrossVoice Tie
      c8 ^~ c4. b8
    } \\
    \new Voice {
      \voiceTwo
      <e, g c>8 <d f>
    }
  >>
}

