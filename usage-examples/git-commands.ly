\version "2.16.0"

#(define moduleName "git-commands")
\include "../includes/oll-example.ily"


\markup \section "Usage:"

\markup \justify { 
  The generic function \ollCommand gitCommand can be used to invoke a Git
  command and print its result. The command expects a string with the Git
  command without the \typewriter git keyword, e.g. \typewriter 
  { rev-parse --short HEAD }. Please note that only the first line of that
  command will be considered. The result is returned as a \ollCommand markup
  \ollCommand column{}. Please be very careful with commands that might 
  actually \italic modify the repository because no checks will be done
  whatsoever. You're on your own risk here!
}

\markup \justify {
  Usually you will use one of the predefined commands listed below.
}

\markup \section "Examples:"
\markup \justify {
  The module contains a number of predefined commands that you can use
  immediately. Of course you can also take them as an inspiration to make
  alternative uses of \ollCommand gitCommand or to write more predefined
  commands. (Feel free to submit additional commands via pull requests
  on the Github project site.
}

\markup \vspace #1

\markup \line {
  \ollCommand gitCommitish
  "- Latest commit (committish): "
}
\markup \typewriter \gitCommitish
\markup \vspace #0.25

\markup \line {
  \ollCommand gitCommit
  "- Latest commit (shortlog):"
}
\markup \typewriter \gitCommit
\markup \null

\markup \line {
  \ollCommand gitFullCommit
  - "Latest commit (full message):"
}
\markup \null
\markup \small \typewriter \gitFullCommit
\markup \vspace #0.25
\markup \italic "(Note that the formatting with typewriter font has been done manually)"
\markup \null

\markup \line {
  \ollCommand gitDateTime
  "- Latest commit (date/time):"
}
\markup \typewriter \gitDateTime
\markup \null


\markup \line {
  \ollCommand gitAuthor
  "- Latest commit (author):"
}
\markup \typewriter \gitAuthor
\markup \null

\markup \line {
  \ollCommand gitEmail
  "- Latest commit (email):"
}
\markup \typewriter \gitEmail
\markup \null

\markup \line {
  \ollCommand gitParentCommittish
  "- Parent commit (committish):"
}
\markup \typewriter \gitParentCommittish
\markup \null

\markup \line {
  \ollCommand gitParentCommit
  "- Parent commit (shortlog):"
}
\markup \typewriter \gitParentCommit
\markup \null

\markup \line {
  \ollCommand gitBranch
  "- Current branch:"
}
\markup \typewriter \gitBranch
\markup \null

\markup \line {
  \ollCommand gitRevisionNumber
  "- Number of commits on this branch:"
}
\markup \typewriter \gitRevisionNumber
\markup \null

\markup \line {
  \ollCommand gitIsClean
  "- Is the working tree clean or does it have uncommitted changes?"
}
\markup \justify {
  This command returns a boolean value depending on the output of \typewriter
  { git status }. You can use its result as a condition for further action.
  If you want to use it to print status information you have to build your
  own markup command around it or use the following command with arguments.
}
\markup \vspace #1
  
\markup \line {
  \ollCommand gitIsCleanMarkup
  "- returns custom markup depending on the repository state."
}
\markup \justify {
  This markup command takes two string arguments specifying the output strings
  to be used for each of the two states. 
}
\markup \line { "The current repository" 
                \bold \gitIsCleanMarkup "has no" "does have"
                  "uncommitted changes" }
\markup \vspace #0.25


\markup \bold "Printing the full Git diff"
\markup \null
\markup \justify {
  In some cases it may be interesting to print out a full diff
  against the latest commit. Usually one compiles scores
  \italic after modifying them and \italic before committing them.
  So if you really need to have a detailed documentation in the
  printout you can supply the full diff as an additional resource.
  Of course it will make sense to provide it on a separate (last)
  page or even in a separate score or bookpart in order not to
  disturb the score layout. Please note that you're responsible
  yourself for any formatting.
}

\markup \vspace #1

 
\markup {
  \override #'(baseline-skip . 2)
  \tiny \typewriter
  \gitDiff
}