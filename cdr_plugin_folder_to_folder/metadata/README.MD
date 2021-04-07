## The Metadata module

The Metadata_Service class manages the creation and updating of the metadata.json files in the HASH directories on HD2

`get_metadata` - takes the path of the file and creates the JSON object
`get_from_file` - get the JSON object from the metadata.json file in the HASH directory
`write_metadata_to_file` - saves the current JSON object to metadata.jsom file in the HASH directory
`get_original_file_path` - obtains the original file path from metadata in the HASH directory
`get_status` - gets current status stored in the metadate.json file of the HASH directory 
`set_status` - updates the status stored in the metadate.json file of the HASH directory 