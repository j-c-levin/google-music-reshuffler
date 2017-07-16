from gmusicapi import Mobileclient
import random
import getpass
import io
# Make a variable of the import
mc = Mobileclient()
# Id of reshuffled playlist
# Put the id in console in here after the first run
reshuffled_playlist_id = '1b350d6e-d170-4863-982f-78a13ccf918b'
# Gmail
email = input('What is your gmail address? ')
# Password
password = getpass.getpass('What is your gmail password (not saved)?')
# Log in
logged_in = mc.login(email, password, mc.FROM_MAC_ADDRESS)
if logged_in is False:
    raise Exception('could not log in', logged_in)
# Number of songs to have in reshuffled album
number_of_songs_in_album = input('How many songs would you like in the album? ')
# If an invalid integer is input, loop until a valid one is
if number_of_songs_in_album.isdigit() == False:
    invalid_input = True
    while invalid_input == True:
        number_of_songs_in_album = input('Please use only an integer, how many songs would you like in the album? ')
        if number_of_songs_in_album.isdigit() == True:
            invalid_input = False
# Convert the song count to an integer
number_of_songs_in_album = int(number_of_songs_in_album)
# Determine if playlist exists
playlists = mc.get_all_playlists()
playlist_already_exists = False
for playlist in playlists:
    if playlist.get('id') == reshuffled_playlist_id:
        print('Found re-shuffler, not recreating')
        playlist_already_exists = True
# Create the reshuffler playlist if it does not exist
if playlist_already_exists != True:
    print('Creating reshuffler album for first time')
    # Create the reshuffler playlist
    playlist_id = mc.create_playlist(
        'Reshuffler', 'A randomly generated and updated playlist of songs, reshuffled')
    print('new id:', playlist_id)
# Get all songs
songs = mc.get_all_songs()
# Create a list for the reshuffled playlist
reshuffled_songs = []
used_index = []
# Randomly select songs
print('Selecting ', number_of_songs_in_album, ' unique songs to add')
for i in range(0, number_of_songs_in_album):
    unused_index = False
    index = -1
    # Ensure no duplicate songs in the playlist
    while (unused_index == False):
        # Randomly select a number from the total length of songs
        index = random.randint(0, len(songs) - 1)
        try:
            # Will error if the number has not already been used
            used_index.index(index)
        except ValueError:
            # If it errors, add the value and continue
            used_index.append(index)
            # Break out of the loop
            unused_index = True
    reshuffled_songs.append(songs[index])
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