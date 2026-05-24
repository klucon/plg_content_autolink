# plg_content_autolink

Plugin pro automatické interní odkazy v článcích.

## Metadata

| Pole | Hodnota |
| :--- | :--- |
| Typ | `plugin` |
| Verze | `0.1.0` |
| Vendor | `klucon` |
| Extension ID | `klucon/plg_content_autolink` |
| Kategorie | `content` |
| Licence | MIT |
| Core minimum | `0.2.15` |
| Python | `>=3.12` |
| Entry point | `src.plugins.plg_content_autolink` |
| Repository | `https://github.com/klucon/plg_content_autolink` |

## Účel

Plugin poslouchá hook `content.article.saved`. Po konfiguraci slovníku `terms` umí v obsahu článku doplnit první výskyt výrazu jako interní odkaz.

## Poznámky k verzi

První verze se settings schématem `terms` a bezpečnou úpravou pouze při explicitní konfiguraci.
