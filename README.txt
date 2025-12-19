- You should only need to run/edit main.py.

- Change the 'shapes' variable as needed.

- Coordinates are (ROW,COL). (0,0) is the top-left corner. From there, count ROW steps down, then COL steps to the right, tracing an L.

- Existing hits and misses speed up the initial generation. In the current algo, the latter has a bigger impact on set-up time.

- If starting from scratch, expect about 4 mins of waiting at the start. Algo enjoyers, please take a look to see if it can be made more efficient!

- If you have a shape combination not in 'combos.txt' and are starting from scratch, please do drop a PR to update the list.

- If you ever notice a symmetrical shape (i.e. not SCARF or CANE) with a mirrored texture, that means that shape has twice as many skins. It will not affect the probability distribution, but yikes.

- I have not done nearly enough stress testing, particularly with user input error handling. Please let me know if anything goes wrong.