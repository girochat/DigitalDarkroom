import os
import pandas as pd
import config
config.DB = pd.DataFrame(columns = ['Event', 'Format', 'Width', 'Height','Megapixels','Channels'
,'Mode','Timestamp', 'Creation','Date_Time','Date','Latitude','Longitude',
'Location','Edited'])
config.DB.to_pickle(os.path.join(config.program_path, "image_DB.pkl")) 
