# RelationFørst

Hjemmeside for RelationFørst (www.relationfoerst.dk). Statiske sider, hostet på Vercel.

## Sådan retter du indhold

1. Ret teksten i `_build/kilde.html` (én lang side med sektionerne `forloeb`, `erfaring`, `tilgang`, `om-os`, `kontakt`).
   Titler, beskrivelser, FAQ og forsidens "Hvem er RelationFørst?" ligger i `_build/build.py`.
2. Kør `python3 _build/build.py`. Det genererer `index.html`, undersiderne, `sitemap.xml` og `llms.txt`.
3. Fælles styling ligger i `styles.css`.
