import streamlit as st
import requests
import json

st.set_page_config(page_title="Spotify Music Player", page_icon="🎧")

st.title("🎧 Spotify RapidAPI Music Player")

RAPIDAPI_KEY = "f3dd6114b8mshe6ff78ae32a91f9p124901jsn4de9f1698693"
RAPIDAPI_HOST = "spotify23.p.rapidapi.com"

headers = {
    'x-rapidapi-key': RAPIDAPI_KEY,
    'x-rapidapi-host': RAPIDAPI_HOST
}

def search_tracks(query):
    url = f"https://{RAPIDAPI_HOST}/search/"
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

def get_track_lyrics(track_id):
    url = f"https://{RAPIDAPI_HOST}/track_lyrics/"
    params = {'id': track_id}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return None

search_query = st.text_input("Search for a song or artist", placeholder="Enter song or artist name...")

if st.button("Search", type="primary"):
    if search_query:
        with st.spinner("Searching..."):
            results = search_tracks(search_query)

            if results and 'tracks' in results and 'items' in results['tracks']:
                tracks = results['tracks']['items']

                if len(tracks) == 0:
                    st.warning("No tracks found. Try a different search.")
                else:
                    st.session_state['tracks'] = tracks
            else:
                st.error("Could not retrieve search results.")
    else:
        st.warning("Please enter a search query.")

if 'tracks' in st.session_state and st.session_state['tracks']:
    st.subheader("Search Results")

    track_options = []
    for track in st.session_state['tracks']:
        track_name = track['data']['name']
        artist_name = track['data']['artists']['items'][0]['profile']['name']
        track_options.append(f"{track_name} - {artist_name}")

    selected_track_index = st.selectbox("Select a track", range(len(track_options)), format_func=lambda x: track_options[x])

    if selected_track_index is not None:
        selected_track = st.session_state['tracks'][selected_track_index]
        track_data = selected_track['data']

        st.markdown("---")

        col1, col2 = st.columns([1, 2])

        with col1:
            album_cover = track_data['albumOfTrack']['coverArt']['sources'][0]['url']
            st.image(album_cover, use_container_width=True)

        with col2:
            st.markdown(f"### {track_data['name']}")
            st.markdown(f"**Artist:** {track_data['artists']['items'][0]['profile']['name']}")
            st.markdown(f"**Album:** {track_data['albumOfTrack']['name']}")

            duration_ms = track_data.get('duration', {}).get('totalMilliseconds', 0)
            duration_sec = duration_ms // 1000
            minutes = duration_sec // 60
            seconds = duration_sec % 60
            st.markdown(f"**Duration:** {minutes}:{seconds:02d}")

        st.markdown("---")

        preview_url = track_data.get('previews', {})
        if preview_url and 'audioPreview' in preview_url and preview_url['audioPreview']:
            audio_url = preview_url['audioPreview']['url']
            st.subheader("🎵 Audio Preview")
            st.audio(audio_url)
        else:
            st.info("⚠️ No audio preview available for this track.")

        st.markdown("---")

        track_id = track_data['uri'].split(':')[-1]

        with st.spinner("Fetching lyrics..."):
            lyrics_data = get_track_lyrics(track_id)

            if lyrics_data and 'lyrics' in lyrics_data:
                st.subheader("📝 Lyrics")

                lyrics_info = lyrics_data['lyrics']

                if 'lines' in lyrics_info:
                    st.markdown(
                        """
                        <style>
                        .lyrics-container {
                            background-color: #f0f2f6;
                            padding: 20px;
                            border-radius: 10px;
                            max-height: 400px;
                            overflow-y: auto;
                        }
                        .lyrics-line {
                            margin: 8px 0;
                            font-size: 16px;
                            line-height: 1.6;
                        }
                        </style>
                        """,
                        unsafe_allow_html=True
                    )

                    lyrics_html = '<div class="lyrics-container">'
                    for line in lyrics_info['lines']:
                        if 'words' in line:
                            lyrics_html += f'<div class="lyrics-line">{line["words"]}</div>'
                    lyrics_html += '</div>'

                    st.markdown(lyrics_html, unsafe_allow_html=True)
                else:
                    st.info("Lyrics structure not available.")
            else:
                st.info("😔 Lyrics not available for this track.")
