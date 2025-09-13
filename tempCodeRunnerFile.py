posters = data.get('posters', [])
    
    if posters:
        # Construct full URLs for posters
        poster_urls = [
            "https://image.tmdb.org/t/p/w500" + poster['file_path']
            for poster in posters
        ]