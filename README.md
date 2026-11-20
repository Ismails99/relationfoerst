# RelationFørst

Hjemmeside for RelationFørst (www.relationfoerst.dk). Statiske sider, hostet på Vercel.

## Sådan retter du indhold

1. Ret teksten i `_build/kilde.html` (sektionerne `forloeb`, `erfaring`, `tilgang`, `om-os`, `kontakt`). Det hele samles på én lang side.
   Titler, beskrivelser, FAQ og forsidens "Hvem er RelationFørst?" ligger i `_build/build.py`.
2. Kør `python3 _build/build.py`. Det genererer `index.html`, `sitemap.xml` og `llms.txt`. Gamle undersider sendes videre via `vercel.json`.
3. Fælles styling ligger i `styles.css`.
