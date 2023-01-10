
background: https://stackoverflow.com/questions/75062701/how-would-i-sever-a-connection-between-islands-in-a-2d-array

> I'm trying to sever potential bridges between islands in a 2d binary matrix.

Which leaves both "island" and "bridge" undefined.

So let's examine a motivating use case.

----

Consider this
[article](https://www.dailymail.co.uk/tvshowbiz/article-2325880/Arrested-Development-brothers-Jason-Bateman-Will-Arnett-hold-hands-stroll-NYC.html)
about a pair of Smartless podcasters having a bit of fun with the paparazzi, which brings us to this photo:
![.](https://i.dailymail.co.uk/i/pix/2013/05/17/article-2325880-19D30C78000005DC-510_634x443.jpg).

----

We will consider
[Von Neumann neighborhoods](https://en.wikipedia.org/wiki/Von_Neumann_neighborhood),
or 4-connected neighborhoods.
The black pixels induce a corresponding planar graph.

Def: a "bridge" is a contiguous sequence of 1s that connects two islands.
