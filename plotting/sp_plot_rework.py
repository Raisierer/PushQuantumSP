import matplotlib.pyplot as plt   
import networkx as nx

class SPPlot():
     def __init__(self, data, evaluation = None):
          self.data = data
          self.evaluation = evaluation

     def plot_solution(self, hide_never_covered = True):
          pos = {node: node for node in self.data.G.nodes()}
          pos_opt= {node: node for node in self.evaluation.O.nodes()}

          if hide_never_covered: 
               street_points_covered = set(self.data.listStreetPoints3D) - set(self.data.listStreetPointsNeverCovered)
               nx.draw_networkx_nodes(self.data.G, pos, nodelist=list(street_points_covered), node_color='blue', node_size=40)
          else: 
               nx.draw_networkx_nodes(self.data.G, pos, self.data.listStreetPoints3D, node_color = 'blue', node_size= 40)
               nx.draw_networkx_nodes(self.data.G, pos, self.data.listStreetPointsNeverCovered, node_color = 'red', node_size= 10)

          nx.draw_networkx_nodes(self.evaluation.O, pos_opt, self.evaluation.listStreetPointsCovered, node_color = 'green', node_size= 40)
          nx.draw_networkx_nodes(self.data.G, pos, self.data.listLidar3D, node_color = 'orange', node_size= 40)
          nx.draw_networkx_nodes(self.evaluation.O, pos_opt, self.evaluation.listLidarActivated, node_color = 'red', node_size= 40)
          
          posw = {node: node for node in self.data.M.nodes()}
          edw = {node: node for node in self.data.M.edges()}
          
          nx.draw_networkx_edges(self.data.M,posw, edw, width=5.0, alpha=1, edge_color='black')

          plt.axis('equal')
          plt.grid(True)
          
          plt.title("Solution")
          plt.text(0.5, -0.05, f'Activated Lidars: {self.evaluation.get_objective()} \n missing achievable coverage: {self.evaluation.check_solution()["missing_achievable_coverage"]}', fontsize=10, ha='center', va='top', transform=plt.gca().transAxes)
          plt.plot
          return plt


     def plot_problem(self, draw_connections = True, hide_never_covered = True, show = False):
          print({self.data.G.nodes[node]["pos"]: self.data.G.nodes[node]["pos"] for node in self.data.G.nodes()})

          g = self.data.G
          g_nodes = g.nodes

          pos = {node: g_nodes[node]["pos"][0:2] for node in g_nodes()}


          lidars = []
          streetpoints = []

          for node in g_nodes:
               
               ty = g_nodes[node]["type"]
               match ty:
                    case x if "lidar" in x:
                         lidars.append(node)
                    case x if "streetpoint" in x:
                         streetpoints.append(node)
                    case _: 
                         continue

          if hide_never_covered: 
               street_points_covered = set(self.data.listStreetPoints3D) - set(self.data.listStreetPointsNeverCovered)
               nx.draw_networkx_nodes(g, pos, nodelist=streetpoints, node_color='blue', node_size=40)
          else: 
               nx.draw_networkx_nodes(g, pos, streetpoints, node_color = 'blue', node_size= 40)
               nx.draw_networkx_nodes(g, pos, self.data.listStreetPointsNeverCovered, node_color = 'red', node_size= 10)

          nx.draw_networkx_nodes(g, pos, lidars, node_color = 'orange', node_size= 40)

          posw = {node: node for node in self.data.M.nodes()}
          edw = {node: node for node in self.data.M.edges()}
          nx.draw_networkx_edges(self.data.M, posw, edw, width=5.0, alpha=1, edge_color='black')

          if draw_connections: 
               nx.draw_networkx_edges(g, pos, width=2.0, alpha=0.5, edge_color='green')

          nx.draw_networkx_labels(g, pos)

          plt.axis('equal')
          plt.grid(True)

          return plt


