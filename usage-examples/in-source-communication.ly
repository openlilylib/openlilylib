\version "2.16.2"

\include "oll-usage-example.ily"

% Activate devMode
\devModeOn

\markup \section \ollCommand comment

\markup \justify {
  A \ollCommand comment does \italic not produce a compiler message as it serves
  more as a mere comment. Compared to a regular source comment it provides a
  consistent syntax and a reference to the affected grob. When \typewriter devMode
  is active the grob will be colored with \typewriter {dev-mode-color-comment} 
  (default: \typewriter {darkgreen)}.
}

\relative c' {
  c 
    \comment Script "Tenuto as per original edition"
    d-- e f\f
}

\markup \section \ollCommand discuss

\markup \justify {
  This command is primarily intended for communication between different editors
  of a score document. It will pretty-print a console message and (with
  \typewriter devMode enabled) color the affected grob with \typewriter
  dev-mode-color-discuss (default: \typewriter {green)}.
  When the discussed topic is finished the command should be either removed or
  changed to \ollCommand comment.
}

\relative c' {
  c d--
    \discuss NoteHead "Why not a square note head?"
    e f\f
}

\markup { \section { \ollCommand todo and \ollCommand followup } }

\markup \justify {
  A TODO item is very similar to the previous "\"discuss\"" command, with two
  differences: The \typewriter dev-mode-color-todo color is \typewriter magenta,
  and the object is colored regardless of \typewriter devMode being active or not.
  This is in order to keep the TODO item visible in any case. To print affected
  items in black nevertheless, there are two options: changing the command to \ollCommand
  comment and overriding the color variable to black.
}

\relative c' {
  c d-- e 
    \todo DynamicText "This dynamic must be checked against manuscript 1"
    \followup "Urs Liska" "I don't think so"
    f\f
}

