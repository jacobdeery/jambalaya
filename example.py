import random
import jambalaya as jb


client = jb.Client()

spec = jb.load_spec('spec_1.yaml')

pl_name = spec['name']
pl_song_ids = jb.get_song_ids(client, spec)

pl_id = client.get_playlist(pl_name)['id']

client.set_playlist(pl_id, pl_song_ids)
