import pandas as pd
import numpy as np
import json
from graphviz import Digraph
import matplotlib.pyplot as plt


class Report:
    def __init__(self, scenario, file_id):
        self.scenario = scenario
        self.file_id = file_id


    def get_path_to_hash(self):
        scenario = self.scenario
        return '/home/jovyan/test_data/'+scenario+'/hd2/status/hash.json'


    def get_hash_data(self):
        path_to_hash = self.get_path_to_hash()
        with open(path_to_hash) as json_file:
            data = json.load(json_file)
        return data


    def get_files(self):
        data = self.get_hash_data()
        files = [elem['file_name'] for elem in data]
        return files


    def get_path_to_report(self):
        scenario = self.scenario
        file_id = self.file_id

        data = self.get_hash_data()
        folder_hash = data[file_id]['original_hash']

        return '/home/jovyan/test_data/'+scenario+'/hd2/data/'+folder_hash+'/report.json'


    def get_dict_from_report(self):
        path_to_report = self.get_path_to_report()
        df0 = pd.read_json(path_to_report)
        df0 = df0.reset_index()

        return df0.iloc[3]['gw:GWallInfo']


    def get_df_from_report(self):
        info = self.get_dict_from_report()
        return pd.DataFrame.from_dict(info)


    def print_document_summary(self):
        info = self.get_dict_from_report()
        d = info['gw:DocumentSummary']

        for key in d:
            d[key] = [d[key]]

        document_summary = pd.DataFrame.from_dict(d)

        document_summary.rename(columns={'gw:TotalSizeInBytes':'Total Size In Bytes',  
                                         'gw:FileType':'File Type',
                                         'gw:Version':'Version'}, inplace=True)

        print('Total Size In Bytes :', document_summary['Total Size In Bytes'].iloc[0])
        print('File Type :', document_summary['File Type'].iloc[0])
        print('Version :', document_summary['Version'].iloc[0])


    def print_extracted_items(self):

        info = self.get_dict_from_report()
        d = info['gw:ExtractedItems']

        for key in d:
            d[key] = [d[key]]

        extracted_items = pd.DataFrame.from_dict(d)

        extracted_items.rename(columns={'@itemCount':'Item Count'}, inplace=True)

        print("Item Count :", extracted_items['Item Count'].iloc[0])


    def content_management_policy_df(self):

        info = self.get_dict_from_report()
        d = info['gw:ContentManagementPolicy']['gw:Camera']

        df0 = pd.DataFrame.from_dict(d)

        data = info['gw:ContentManagementPolicy']['gw:Camera'][0]['gw:ContentSwitch']

        if len(data) == 2:
            for key in data:
                data[key] = [data[key]]

        df = pd.DataFrame.from_dict(data)
        df['@cameraName'] = df0.iloc[0]['@cameraName']
        df = df[['@cameraName', 'gw:ContentName', 'gw:ContentValue']]

        for i in range(1, len(df0)):
            data = info['gw:ContentManagementPolicy']['gw:Camera'][i]['gw:ContentSwitch']

            if len(data) == 2:
                for key in data:
                    data[key] = [data[key]]

            df1 = pd.DataFrame.from_dict(data)
            df1['@cameraName'] = df0.iloc[i]['@cameraName']
            df1 = df1[['@cameraName', 'gw:ContentName', 'gw:ContentValue']]

            df = pd.concat([df, df1], ignore_index=True)


        df.rename(columns={'@cameraName':'Camera Name', 
                           'gw:ContentName':'Content Name', 
                           'gw:ContentValue':'Content Value'}, inplace=True) 
        return df


    def camera_graph(self, camera_value):

        content_management_policy = self.content_management_policy_df()

        gra = Digraph()

        # root node
        elem = camera_value
        gra.node(elem, shape='box')

        df0 = content_management_policy[content_management_policy['Camera Name']==elem]

        content_name = list(df0['Content Name'].unique())

        with gra.subgraph() as i:
            i.attr(rank='same')   
            for elem2 in content_name:
                i.node(elem2, shape='box')

        for elem2 in content_name:
            df00 = df0[df0['Content Name']==elem2]
            k = int(df00.index[0])
            text = df00.iloc[0]['Content Value']
            gra.node(str(k), text, shape='box')
            gra.edge(elem2, str(k))

        for elem3 in df0['Content Name']:
            gra.edge(elem, elem3)

        return gra


    def get_num_of_groups(self, text=False):
        info = self.get_dict_from_report()
        num_groups = info['gw:ContentGroups']['@groupCount']
        if text:
            print("There are " + num_groups + " groups")
        else:
            return num_groups


    def content_groups_df(self):
        info = self.get_dict_from_report()
        d = info['gw:ContentGroups']['gw:ContentGroup'][0]['gw:ContentItems']['gw:ContentItem']

        df = pd.DataFrame.from_dict(d)
        df['gw:BriefDescription'] = info['gw:ContentGroups']['gw:ContentGroup'][0]['gw:BriefDescription']
        df = df[['gw:BriefDescription', 'gw:TechnicalDescription', 'gw:InstanceCount', 'gw:TotalSizeInBytes', 'gw:AverageSizeInBytes', 'gw:MinSizeInBytes', 'gw:MaxSizeInBytes']]

        num_groups = self.get_num_of_groups()
        for i in range(1, int(num_groups)):

            df1 = pd.DataFrame.from_dict(d)
            df1['gw:BriefDescription'] = info['gw:ContentGroups']['gw:ContentGroup'][i]['gw:BriefDescription']
            df1 = df1[['gw:BriefDescription', 'gw:TechnicalDescription', 'gw:InstanceCount', 'gw:TotalSizeInBytes', 'gw:AverageSizeInBytes', 'gw:MinSizeInBytes', 'gw:MaxSizeInBytes']]

            df = pd.concat([df, df1], ignore_index=True)

        df.rename(columns={'gw:BriefDescription':'Brief Description', 
                           'gw:TechnicalDescription':'Technical Description',
                           'gw:InstanceCount':'Instance Count',
                           'gw:TotalSizeInBytes':'Total Size In Bytes',
                           'gw:AverageSizeInBytes':'Average Size In Bytes',
                           'gw:MinSizeInBytes':'Min Size In Bytes',
                           'gw:MaxSizeInBytes':'Max Size In Bytes'}, inplace=True)
        return df


    def group_df(self, group_value):
        content_groups = self.content_groups_df()
        df0 = content_groups[content_groups['Brief Description']==group_value]
        df1 = df0.set_index('Technical Description')

        df1["Instance Count"] = pd.to_numeric(df1["Instance Count"])
        df1["Total Size In Bytes"] = pd.to_numeric(df1["Total Size In Bytes"])
        df1["Average Size In Bytes"] = pd.to_numeric(df1["Average Size In Bytes"])
        df1["Min Size In Bytes"] = pd.to_numeric(df1["Min Size In Bytes"])
        df1["Max Size In Bytes"] = pd.to_numeric(df1["Max Size In Bytes"])

        df1 = df1.drop(columns='Brief Description')
        return df1


    def group_graph(self, group_value):
        gra = Digraph()

        # root node
        elem = group_value
        gra.node(elem, shape='box')

        content_groups = self.content_groups_df()
        df0 = content_groups[content_groups['Brief Description']==group_value]
        tech_description = list(df0['Technical Description'].unique())

        with gra.subgraph() as i:
            i.attr(rank='same')
            for elem2 in tech_description:
                i.node(elem2, shape='box')

        for elem3 in df0['Technical Description']:
            gra.edge(elem, elem3)

        for elem2 in tech_description:
            k = tech_description.index(elem2)
            df00 = df0[df0['Technical Description']==elem2].reset_index()
            text = 'Instance Count: ' + df00['Instance Count'].iloc[0]
            text += '\nTotal Size In Bytes: ' + df00['Total Size In Bytes'].iloc[0]
            text += '\nAverage Size In Bytes: ' + df00['Average Size In Bytes'].iloc[0]
            text += '\nMin Size In Bytes: ' + df00['Min Size In Bytes'].iloc[0]
            text += '\nMax Size In Bytes: ' + df00['Max Size In Bytes'].iloc[0]

            gra.node(str(k), text, shape='box')
            gra.edge(elem2, str(k))

        return gra


    def get_group_tech_descriptions(self, group_value):
        content_groups = self.content_groups_df()
        df0 = content_groups[content_groups['Brief Description']==group_value]
        return list(df0['Technical Description'].unique())


    def group_instance_count(self, group_value):
        df1 = self.group_df(group_value)

        with plt.style.context('ggplot'):
            plt.figure(figsize=(15, 8))
            df1['Instance Count'].plot(kind='bar', color='C0', title='Instance Count')


    def group_tech_barchart_1(self, group_value, tech_value):
        df1 = self.group_df(group_value).T

        with plt.style.context('ggplot'):
            plt.figure(figsize=(15,8))
            df1[tech_value].plot(kind='bar', color='C0', title=tech_value);


    def group_tech_barchart_2(self, group_value, tech_value):
        df1 = self.group_df(group_value).T
        labels = [tech_value]

        count = [df1[tech_value].iloc[0]]
        total = [df1[tech_value].iloc[1]]
        average = [df1[tech_value].iloc[2]]
        min_ = [df1[tech_value].iloc[3]]
        max_ = [df1[tech_value].iloc[4]]

        x = np.arange(len(labels))  # the label locations
        width = 0.25  # the width of the bars

        fig, ax = plt.subplots(figsize=(15, 8))
        rects1 = ax.bar(x - 2*width, count, width, label='Instance Count')
        rects2 = ax.bar(x - width, total, width, label='Total Size In Bytes')
        rects3 = ax.bar(x , average, width, label='Average Size In Bytes')
        rects4 = ax.bar(x + width, min_, width, label='Min Size In Bytes')
        rects5 = ax.bar(x + 2*width, max_, width, label='Max Size In Bytes')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_title(tech_value)
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()

        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)
        ax.bar_label(rects3, padding=3)
        ax.bar_label(rects4, padding=3)
        ax.bar_label(rects5, padding=3)

        fig.tight_layout()

        plt.show()

