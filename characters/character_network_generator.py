import os
import pandas as pd
import networkx as nx
from pyvis.network import Network

class CharacterNetworkGenerator:
    def __init__(self):
        pass

    def generate_char_network(df):

        windows = 10
        entity_relationship = []

        for row in df["chars"]:
            prev_entity_window = []

            for sentence in row:
                
                # each sentence = ["Ted", "Lilly"]
                prev_entity_window.append(list(sentence))

                # We keep only the last 10 entities as previous.
                prev_entity_window = prev_entity_window[-windows:]

                # Flatten 2D list into 1D list
                prev_entity_flattened = sum(prev_entity_window, [])

                # Build relationship for each entity.
                for entity in sentence:
                    # Check each entity with all previous 10 entities.
                    for entity_in_window in prev_entity_flattened:

                        # if they aren't same, append them because they are related.
                        if entity != entity_in_window:

                            # Sort them because (ted, lilly is same as lilly, ted.)
                            entity_relationship.append(sorted([entity, entity_in_window]))

        relationship_df = pd.DataFrame({"value": entity_relationship})
        relationship_df["source"] = relationship_df["value"].apply(lambda x: x[0])
        relationship_df["target"] = relationship_df["value"].apply(lambda x: x[1])
        relationship_df = relationship_df.groupby(["source", "target"]).count().reset_index()
        relationship_df = relationship_df.sort_values("value", ascending=False)

        return relationship_df
    
    def draw_char_network(self, df):

        df = df.sort_values("value", ascending=False).head(200)

        G = nx.from_pandas_edgelist(
            df,
            source="source",
            target="target",
            edge_attr="value",
            create_using=nx.Graph()
        )

        net = Network(
            notebook=True, width="1000px", 
            height="700px", 
            bgcolor="#222222", 
            font_color="white", 
            cdn_resources="remote"
        )

        node_degree = dict(G.degree)

        nx.set_node_attributes(G, node_degree, "size")
        net.from_nx(G)

        html = net.generate_html()
        html = html.replace("'", "\"")

        output_html = f"""<iframe style="width: 100%; height: 600px;margin:0 auto" name="result" allow="midi; geolocation; microphone; camera;
        display-capture; encrypted-media;" sandbox="allow-modals allow-forms
        allow-scripts allow-same-origin allow-popups
        allow-top-navigation-by-user-activation allow-downloads" allowfullscreen=""
        allowpaymentrequest="" frameborder="0" srcdoc='{html}'></iframe>"""
        
        return output_html

    def defaultGraph(self, save_path):


        if save_path and not save_path.endswith(".html"):
            save_path += "network.html"
            
        with open("characters\himym.html", "r") as f:
            html = f.read()

        html = html.replace("'", "\"")

        output_html = f"""<iframe style="width: 100%; height: 600px;margin:0 auto" name="result" allow="midi; geolocation; microphone; camera;
        display-capture; encrypted-media;" sandbox="allow-modals allow-forms
        allow-scripts allow-same-origin allow-popups
        allow-top-navigation-by-user-activation allow-downloads" allowfullscreen=""
        allowpaymentrequest="" frameborder="0" srcdoc='{html}'></iframe>"""

        try: 
            if save_path:
                with open("../" + save_path, "w") as f:
                    f.write(output_html)
        except:
            pass     
        return output_html
    
print(CharacterNetworkGenerator().defaultGraph("cache"))