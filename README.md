# Postfacto Happiness Grapher

This was a quick and dirty project to calculate happiness over time
based on the amount of happy, meh and sad cards posted in postfacto

## Getting the data

```bash
# Download from the archives. Open the first archived retro and check the id in the url
# Mine started at 114 and ended at 236
# Also change the `retros/waifsandstrays` to suit your board
for x in $(seq 114 236); do curl -H 'authorization: Bearer eyJhb...' https://postfacto.domain.com/api/retros/waifsandstrays/archives/$x -o data/$x.json; done

# Remove files that are empty (contain `{}`)
find ./data -size -3c -exec rm {} \;
```

> You can get the `Bearer` header by simply opening up the inspect element menu when on Postfacto (once logged in), refreshing the page and looking for the sent headers of a request

## TODO
- Make readme look good