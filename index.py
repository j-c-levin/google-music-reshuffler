from gmusicapi import Mobileclient
import random
# Make a variable of the import
mc = Mobileclient()
# Number of songs to have in reshuffled album
number_of_songs_in_album = 100
# Id of reshuffled playlist
# Put the id in console in here after the first run
reshuffled_playlist_id = '1b350d6e-d170-4863-982f-78a13ccf918b'
# Gmail
email = ''
# Password
password = ''
# Log in
logged_in = mc.login(email, password, mc.FROM_MAC_ADDRESS)
# Determine if playlist exists
playlists = mc.get_all_playlists()
playlist_already_exists = False
for playlist in playlists:
    if playlist.get('id') == reshuffled_playlist_id:
        print('Found re-shuffler, not recreating')
        playlist_already_exists = True
# Create the reshuffler playlist if it does not exist
if playlist_already_exists == False:
    print('Creating reshuffler album for first time')
    # Create the reshuffler playlist
    playlist_id = mc.create_playlist(
        'Reshuffler', 'A randomly generated and updated playlist of songs, reshuffled')
    print('new id:', playlist_id)
# Get all songs
songs = mc.get_all_songs()
# Create a list for the reshuffled playlist
reshuffled_songs = []
# Randomly select songs
print('Selecting ', number_of_songs_in_album, ' songs to add')
for i in range(0, number_of_songs_in_album):
    index = random.randint(0, len(songs) - 1)
    reshuffled_songs.insert(i, songs[index])
# Get all current songs in the reshuffled playlist
current_songs = mc.get_all_user_playlist_contents()
# Delete all songs from current playlist
for playlist in current_songs:
    # Find the correct playlist
    if playlist.get('id') == reshuffled_playlist_id:
        print('Deleting ', len(playlist.get('tracks')),
              ' old songs from the reshuffled playlist')
        # Iterate over the tracks in it
        for song in playlist.get('tracks'):
            mc.remove_entries_from_playlist(song.get('id'))
# Add new to playlist
print('Adding new songs')
for song in reshuffled_songs:
    mc.add_songs_to_playlist(reshuffled_playlist_id, song.get('id'))
# End
print('Done')
