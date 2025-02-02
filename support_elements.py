list_of_playlist_id = [
    'PL5-QUghxmluKdvUZzlP5yFZ-nxz_qGPpp',
    'PLvuwbYTkUzHe7lCkOX_m2Y1ugcRV661kd',
    'PLCQm3OPgov-jjAejMWJplRNIdfKSE9v5G',
    'PLR8DItC4f5xvbI5uqur4rsoTOMmk7F5SQ',
    'PLp_A7BZlpSOcTIR2PSiCU9Q7x_9eAWr9F',
    'PLCQm3OPgov-jS8Y1TJ7mlsmH-OSYPaRs6',
    'PLx6bGx4zt6Enox9Gh0C5QqU2dVu4EdMjI',
    'PLx6bGx4zt6ElKsh4RyN4MKCQs5nGHNOyA',   
]

title_patterns = [
                r'([a-zA-Z &]+)\s(\d+)-(\d+)\s([a-zA-Z &]+)',  # Team1 2-1 Team2
                r'([a-zA-Z &]+)\s+vs\s+([a-zA-Z &]+)\s*\((\d+)-(\d+)\)',  # Team1 vs Team2 (2-1)
                r'([a-zA-Z &]+)\s+v\.?\s+([a-zA-Z &]+)\s+(\d+)-(\d+)',  # Team1 v Team2 2-1
                r'([a-zA-Z &]+)\s+(\d+)\s*[-:]\s*(\d+)\s+([a-zA-Z &]+)',  # Team1 2:1 Team2
                r'([a-zA-Z &]+?)\s*\((\d+)\)\s*(?:vs\.?)?\s*([a-zA-Z &]+?)\s*\((\d+)\)',  # Team1 (2) vs Team2 (1)
                r'([a-zA-Z &]+)\s+vs\.?\s+([a-zA-Z &]+)\s+(\d+)\s*-\s*(\d+)',  # Team1 vs Team2 2-1
                r'([a-zA-Z &]+?)(?:\s+|-)(\d+)\s*-\s*(\d+)(?:\s+|-)([a-zA-Z &]+)'  # Team1-2-1-Team2 or Team1 2-1 Team2
            ]

football_competition = [
        'Premier League',
        'UEFA Conference League',
        'Carabao Cup',
        'FA Cup',
        'Champions League',
        'UEFA Champions League',
        'Europa League',
        'UEFA Europa League'
    ]