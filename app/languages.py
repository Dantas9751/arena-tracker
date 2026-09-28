# -----------------------------------------------------------------------------
# IDIOMA ATIVO
# -----------------------------------------------------------------------------
# Troque aqui para "en-US" se o cliente do LoL estiver em inglês.
LANGUAGE = "pt-BR"

TESSERACT_LANG_CODES = {
    "pt-BR": "por",
    "en-US": "eng",
}

# -----------------------------------------------------------------------------
# ITENS PRISMÁTICOS (PT-BR <-> EN-US)
# -----------------------------------------------------------------------------
PRISMATIC_ITEMS_I18N = [
    {"pt-BR": "Manopla do Buraco Negro", "en-US": "Black Hole Gauntlet"},
    {"pt-BR": "Capa do Piromante", "en-US": "Pyromancer's Cloak"},
    {"pt-BR": "Coroa da Rainha Despedaçada", "en-US": "Crown of the Shattered Queen"},
    {"pt-BR": "Crueldade", "en-US": "Cruelty"},
    {"pt-BR": "Garras de Aço Sombrio", "en-US": "Darksteel Talons"},
    {"pt-BR": "Decapitador", "en-US": "Decapitator"},
    {"pt-BR": "Coroa do Rei Demoníaco", "en-US": "Demon King's Crown"},
    {"pt-BR": "Abraço Demoníaco", "en-US": "Demonic Embrace"},
    {"pt-BR": "Orbe da Detonação", "en-US": "Detonation Orb"},
    {"pt-BR": "Lança de Diamante", "en-US": "Diamond-Tipped Spear"},
    {"pt-BR": "Coração Dracônico", "en-US": "Dragonheart"},
    {"pt-BR": "Lâmina do Crepúsculo de Draktharr", "en-US": "Duskblade of Draktharr"},
    {"pt-BR": "Milagre de Eleisa", "en-US": "Eleisa's Miracle"},
    {"pt-BR": "Promessa Empírea", "en-US": "Empyrean Promise"},
    {"pt-BR": "Glacieterno", "en-US": "Everfrost"},
    {"pt-BR": "Comecarne", "en-US": "Flesheater"},
    {"pt-BR": "Força da Entropia", "en-US": "Force of Entropy"},
    {"pt-BR": "Fulminação", "en-US": "Fulmination"},
    {"pt-BR": "Força do Vendaval", "en-US": "Galeforce"},
    {"pt-BR": "Lâmina do Apostador", "en-US": "Gambler's Blade"},
    {"pt-BR": "Placa Gargolítica", "en-US": "Gargoyle Stoneplate"},
    {"pt-BR": "Hemodrenário", "en-US": "Goredrinker"},
    {"pt-BR": "Debilitador", "en-US": "Hamstringer"},
    {"pt-BR": "Elmo Hemomante", "en-US": "Hemomancer's Helm"},
    {"pt-BR": "Companheiro Hexraio", "en-US": "Hexbolt Companion"},
    {"pt-BR": "Medalhão Enervante", "en-US": "Innervating Locket"},
    {"pt-BR": "Jitte Kinkou", "en-US": "Kinkou Jitte"},
    {"pt-BR": "Bastão Eletrizante", "en-US": "Lightning Rod"},
    {"pt-BR": "Espada da Miragem", "en-US": "Mirage Blade"},
    {"pt-BR": "Lâmina Enfeitiçada Moonflair", "en-US": "Moonflair Spellblade"},
    {"pt-BR": "Colhedor Noturno", "en-US": "Night Harvester"},
    {"pt-BR": "Garra do Espreitador", "en-US": "Prowler's Claw"},
    {"pt-BR": "Titereiro", "en-US": "Puppeteer"},
    {"pt-BR": "Virtude Radiante", "en-US": "Radiant Virtue"},
    {"pt-BR": "Fenda Dimensional", "en-US": "Reality Fracture"},
    {"pt-BR": "Colheita do Ceifador", "en-US": "Reaper's Toll"},
    {"pt-BR": "Regicídio", "en-US": "Regicide"},
    {"pt-BR": "Reverberação", "en-US": "Reverberation"},
    {"pt-BR": "Criarrunas", "en-US": "Runecarver"},
    {"pt-BR": "Presente Sanguinário", "en-US": "Sanguine Gift"},
    {"pt-BR": "Escudo de Rocha Fundida", "en-US": "Shield of Molten Stone"},
    {"pt-BR": "Espada do Divino", "en-US": "Sword of the Divine"},
    {"pt-BR": "Talismã da Ascensão", "en-US": "Talisman of Ascension"},
    {"pt-BR": "Quimiotanque Turbo", "en-US": "Turbo Chemtank"},
    {"pt-BR": "Limite do Crepúsculo", "en-US": "Twilight's Edge"},
    {"pt-BR": "Armadura de Warmog", "en-US": "Warmog's Armor"},
    {"pt-BR": "Manto da Noite Estrelada", "en-US": "Cloak of Starry Night"},
    {"pt-BR": "Ruptor Divino", "en-US": "Divine Sunderer"},
]


def get_valid_items(language=LANGUAGE):
    return sorted({entry[language] for entry in PRISMATIC_ITEMS_I18N})


def get_tesseract_lang(language=LANGUAGE):
    return TESSERACT_LANG_CODES[language]
