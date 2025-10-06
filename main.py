import streamlit as st
import requests
import json

st.set_page_config(page_title="Spotify Music Player", page_icon="🎧", layout="wide")

st.title("🎧 Spotify RapidAPI Music Player")

API_KEY = "f3dd6114b8mshe6ff78ae32a91f9p124901jsn4de9f1698693"
API_HOST = "spotify23.p.rapidapi.com"

headers = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': API_HOST
}

def search_tracks(query):
    url = f"https://{API_HOST}/search/"
    params = {
        'q': query,
        'type': 'tracks',
        'limit': 5
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error searching tracks: {str(e)}")
        return None

def get_lyrics(track_id):
    url = f"https://{API_HOST}/track_lyrics/"
    params = {'id': track_id}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return None

st.markdown("### Search for a song or artist")
query = st.text_input("Enter song or artist name:", placeholder="e.g., Billie Eilish")

if st.button("🔍 Search", type="primary"):
    if query:
        with st.spinner("Searching..."):
            results = search_tracks(query)

            if results and 'tracks' in results and 'items' in results['tracks']:
                tracks = results['tracks']['items']

                if tracks:
                    st.success(f"Found {len(tracks)} tracks")

                    for idx, track in enumerate(tracks):
                        with st.expander(f"🎵 {track['name']} - {', '.join([artist['name'] for artist in track['artists']])}", expanded=(idx == 0)):
                            col1, col2 = st.columns([1, 2])

                            with col1:
                                if track.get('album') and track['album'].get('images'):
                                    st.image(track['album']['images'][0]['url'], width=250)
                                else:
                                    st.info("No album cover available")

                            with col2:
                                st.markdown(f"**Song:** {track['name']}")
                                st.markdown(f"**Artist(s):** {', '.join([artist['name'] for artist in track['artists']])}")
                                st.markdown(f"**Album:** {track['album']['name']}")
                                st.markdown(f"**Release Date:** {track['album'].get('release_date', 'N/A')}")

                                if track.get('preview_url'):
                                    st.audio(track['preview_url'])
                                else:
                                    st.warning("⚠️ Preview audio not available for this track")

                            st.markdown("---")
                            st.markdown("### 📝 Lyrics")

                            with st.spinner("Fetching lyrics..."):
                                lyrics_data = get_lyrics(track['id'])

                                if lyrics_data and 'lyrics' in lyrics_data and 'lines' in lyrics_data['lyrics']:
                                    lyrics_lines = lyrics_data['lyrics']['lines']

                                    if lyrics_lines:
                                        st.info("Note: Lyrics display is limited to avoid copyright issues. Please visit Spotify or official sources for complete lyrics.")

                                        lyrics_container = st.container()
                                        with lyrics_container:
                                            st.markdown(
                                                """
                                                <style>
                                                .lyrics-box {
                                                    background-color: #f0f2f6;
                                                    padding: 20px;
                                                    border-radius: 10px;
                                                    max-height: 300px;
                                                    overflow-y: auto;
                                                    font-family: 'Courier New', monospace;
                                                    line-height: 1.6;
                                                }
                                                </style>
                                                """,
                                                unsafe_allow_html=True
                                            )

                                            preview_text = f"Lyrics available ({len(lyrics_lines)} lines)"
                                            st.markdown(f'<div class="lyrics-box">{preview_text}<br><br>🎤 Full lyrics available on Spotify</div>', unsafe_allow_html=True)
                                    else:
                                        st.warning("No lyrics available for this track")
                                else:
                                    st.warning("Lyrics not found for this track")

                            st.markdown("---")
                else:
                    st.warning("No tracks found. Try a different search term.")
            else:
                st.error("Unable to retrieve search results. Please try again.")
    else:
        st.warning("Please enter a search query")

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>Powered by Spotify API via RapidAPI</p>
        <p style='font-size: 0.8em;'>Search for your favorite songs and artists</p>
    </div>
    """,
    unsafe_allow_html=True
)
