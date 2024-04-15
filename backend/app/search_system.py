from services.database import connect
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from backend.app.models import models
from datetime import datetime

app = FastAPI()

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# def search(query):
#     if query == "listings":
#         return search_listings(query)
#     elif query == "profiles":
#         return search_profiles(query)

#     return "search result for: " + query

#example query:http://127.0.0.1:8000/search/listings/?title=movie&description=sci-fi
@app.get("/search/listings/")
def search_listings(title: Optional[str] = None, description: Optional[str] = None): 
    print("HELLO")
    conn = connect()
    cursor = conn.cursor()

    # Prepare SQL query to search for listings based on title or description
    sql_query = '''
        SELECT * FROM listing
        WHERE title LIKE %s OR description LIKE %s
    '''
    values = (
    f'%{title}%',  # Assuming title is the pattern to search for in the title column
    f'%{description}%'  # Assuming description is the pattern to search for in the description column
    )

    # Execute SQL query with search query as parameters
    cursor.execute(sql_query, values)

    # Fetch results from executed query
    listings = cursor.fetchall()
    
    # Format search results
    formatted_listings = []
    for listing in listings:
        formatted_listing = {
            'listing_id': listing[0],
            'user_id': listing[1],
            'date': listing[2],
            'title': listing[3],
            'description': listing[4]
        }
        formatted_listings.append(formatted_listing)
    
    cursor.close()

    return formatted_listings

# @app.get("/search/profiles/{query}")
# def search_profiles(query):
#     query = query.json()
#     conn = connect()
#     cursor = conn.cursor()

#     # Prepare the SQL query to search for profiles based on username, email, or description 
#     sql_query = '''
#         SELECT * FROM users
#         WHERE title LIKE %s OR description LIKE %s
#     '''

#     # Execute the SQL query with the search query as parameters
#     cursor.execute(sql_query, (f'%{query}%', f'%{query}%', f'%{query}%'))

#     # Fetch the results from the executed query
#     profiles = cursor.fetchall()

#     # Format the search results
#     formatted_profiles = []
#     for profile in profiles:
#         formatted_profile = {
#             'user_id': profile[0],
#             'username': profile[1],
#             'email': profile[2],
#             'description': profile[3],
#             'profile_picture': profile[4],
#             'interest1': profile[5],
#             'interest2': profile[6],
#             'interest3': profile[7],
#             'gender': profile[8]
#         }
#         formatted_profiles.append(formatted_profile)

#     cursor.close()
#     return formatted_profiles

    



    