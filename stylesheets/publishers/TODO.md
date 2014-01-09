## Kieren's Styles TODO

This library will be laid out in a directory structure which contains redundant parts.

There will be one directory containing all base functionality and others that
only contain "target" include files.

The directory structure will be `instrument/paper/geometry/publisher`,
e.g.  
`choral/octavo/portrait/`
where the final folder contains include files for specific publishers like  
`choral/octavo/portrait/henle.ily` or  
`piano/concert/portrait/peters.ily`

Any such include file will `\include` relevant detail modules and potentially modifies
them to suit its need.

See the below excerpt from an email conversation.

>> How much shared code will there be?
>> Is choral_octave_portrait_Peters.ly completely independent from
>> choral_octave_portrait_Henle.ly?
>
> Maybe this will help explain what I’m thinking:
>
> “Base” Files:
>      octavo.ly
>      ChoirStaff.ly
>      Peters_house.ly
>      Henle_house.ly
>
> “Building” Files:
>
>      choral_octavo.ly
>           \include ChoirStaff.ly
>           \include octavo.ly
>
>      choral_octavo_portrait.ly
>           \include choral_octavo.ly
>
>      choral_octavo_portrait_Peters.ly
>          \include choral_octavo_portrait.ly
>          \include Peters_house.ly
>
>      choral_octavo_portrait_Henle.ly
>          \include choral_octavo_portrait.ly
>          \include Henle_house.ly
>
>> But if the "concert" stuff would be basically the same for all variants it doesn't seem to be such a good idea to duplicate all these files.
>

I'm not completely sure if I really see everything.
But it may be that the \include "choral/octavo/porait/Henle.ly"
approach might be a good idea. This means that for any combination that is actually implemented/tested you'd need one file:
choral/octavo/porait/Henle.ly is equivalent to
choral_octavo_portrait_Henle.ly.
Then this "target" file includes the other files as needed and still can alter them, e.g.
- include octavo.ly
- but add some Henle specific modifications.
(I'm assuming that all this is within a library that is added to LilyPond's include path, so the files are guaranteed to be found on a specific path.)

Adding a new combination (say: choral/octavo/portrait/Peters) would be a matter of copying and renaming one file, then start to experiment and tweak if necessary.

