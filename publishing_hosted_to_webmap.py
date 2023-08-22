from arcgis.gis import GIS
from arcgis.features import GeoAccessor
from arcgis.mapping import WebMap
import pandas as pd

def create_hosted_file_from_shp(gis, folder_qc, data, host_name):
        gis.content.create_folder(folder_qc)
        df = pd.DataFrame.spatial.from_featureclass(data)
        df.spatial.to_featurelayer(title=host_name,tags="qc,testing,initial,hosted", folder=folder_qc, sanitize_columns=False, service_name='sample')
        
def create_webmap(gis, webmap_name, host_name):
        item_sample = gis.content.search(host_name)[0]

        i_properties_webmap = {
                "title" : webmap_name,
                "snippet": "Automated WebMap",
                "tags": "qc, testing, initial, hosted",
                "description" : "publish hosted using arcgis api python"}
        
        wm = WebMap()
        wm.add_layer(item_sample)
        wm.save(item_properties=i_properties_webmap, folder=folder_qc)

if __name__ == "__main__":
    url = input('Please input portal url: ')
    uname = input('Please input administrator username : ')
    pwd = input('Please input administrator password: ')
    
    folder_qc = input('Please input folder name to be created in portal: ')
    shp_fc = input('Please input data: ')
    
    hosted_name = input('Please input feature class hosted name: ')
    webmap_name = input('Please input webmap name for QC: ')
    
    print('Checking the parameter')
    if folder_qc is None or folder_qc == '':
        folder_qc = 'QC_PUBLISH_HOSTED'
    
    if shp_fc is None or shp_fc == '':
        shp_fc = 'sample.shp'
    
    if webmap_name is None or webmap_name == '':
        webmap_name = 'Webmap - QC - Testing'

    if hosted_name is None or hosted_name == '':
         hosted_name = 'QC_SAMPLE'

    print('Checking the parameter is completed')

    try:
        print('Sign in to arcgis enterprise')
        gis = GIS(url, uname, pwd)
        print('Sign in success')

        print('Processing hosted file')
        create_hosted_file_from_shp(gis, folder_qc, shp_fc, hosted_name)
        print('hosted file is successfully published')

        print('Creating webmap from the published hosted file')
        create_webmap(gis, webmap_name, hosted_name)
        print('Webmap successfully created')

    except Exception as e:
         raise(e)